import numpy as np
import pandas as pd


def main(payload):
    df_list = []
    for key, value in payload.items():
        df = pd.DataFrame(value)
        df = df.set_index("timestamp")

        if not (key is "base"):
            df = df.rename(
                columns={
                    "value": key,
                    "data": key,
                },
            )

        df_list.append(df)

    response_df = pd.concat(df_list, axis=1)
    response_df = response_df.replace({np.nan: None})
    response_df["timestamp"] = response_df.index
    response = response_df.to_dict(orient="records")

    return response
