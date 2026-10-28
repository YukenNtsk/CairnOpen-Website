import pandas as pd
import requests


def get_annual_tilted_irradiance_average(
    lat: float, lon: float, tilt: float = 30, azimuth: float = 0
) -> pd.DataFrame:
    
    """Calcule le profil moyen annuel heure par heure (366 jours x 24h) de l'irradiance

    captée par un panneau incliné/orienté, basé sur les données 2020-2025.

    :param lat: Latitude (ex: 48.8566)
    :param lon: Longitude (ex: 2.3522)
    :param tilt: Inclinaison du panneau en degrés (ex: 30, valeur la plus commune)
    :param azimuth: Orientation du panneau (0 = Sud, -90 = Est, 90 = Ouest) (orientation plein sud est la plus obtimale)
    :return: DataFrame avec la moyenne horaire sur 1 an (G_panneau_W_m2)
    """
    
    # 1. Requête API Open-Meteo avec la variable global_tilted_irradiance
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": "2020-01-01",
        "end_date": "2025-12-31",
        "hourly": ["global_tilted_irradiance"],
        "tilt": tilt,
        "azimuth": azimuth,
        "timezone": "Europe/Paris",
    }

    res = requests.get(url, params=params)
    res.raise_for_status()

    # 2. Construction du DataFrame
    df = pd.DataFrame(res.json()["hourly"])
    df["time"] = pd.to_datetime(df["time"])

    # 3. Extraction des composantes temporelles
    df["month"] = df["time"].dt.month
    df["day"] = df["time"].dt.day
    df["hour"] = df["time"].dt.hour

    # 4. Calcul de la moyenne sur 2020-2025 pour chaque créneau (Mois, Jour, Heure)
    result_df = (
        df.groupby(["month", "day", "hour"])[["global_tilted_irradiance"]]
        .mean()
        .reset_index()
    )

    # 5. Tri chronologique sur l'année complète (utilisation de 2024 pour gérer le 29 février)
    result_df["temp_date"] = pd.to_datetime(
        result_df.assign(year=2024)[["year", "month", "day", "hour"]]
    )
    result_df = (
        result_df.sort_values("temp_date")
        .drop(columns=["temp_date"])
        .reset_index(drop=True)
    )

    # 6. Renommage des colonnes
    result_df.rename(
        columns={
            "month": "Mois",
            "day": "Jour",
            "hour": "Heure",
            "global_tilted_irradiance": "G_panneau_W_m2",
        },
        inplace=True,
    )

    return result_df

get_annual_tilted_irradiance_average(lat=48.8566, lon=2.3522, tilt=30, azimuth=0).head(24)