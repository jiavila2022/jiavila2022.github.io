from flask import Flask, render_template, request, jsonify
import pandas as pd
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns
from algorithm import create_teams, create_df_image
import io
import base64

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/make-teams", methods=["POST"])
def make_teams():
    # Get selected names from JavaScript
    data = request.get_json()

    selected_names = data["names"]
    num_of_teams = data["num_teams"]

    # Load your CSV
    df = pd.read_csv('volleyball_data_transformed.csv')

    # Filter dataframe to selected people
    df = df[df["Name"].isin(selected_names)]

    # ==========================================
    # YOUR EXISTING TEAM ALGORITHM GOES HERE
    
    summarized_df, team_names_df, df = create_teams(df, num_of_teams=num_of_teams)
    
    # Create heatmap
    fig = create_df_image(summarized_df)

    # Convert figure to PNG in memory
    image_buffer = io.BytesIO()

    fig.savefig(
        image_buffer,
        format="png",
        bbox_inches="tight",
        dpi=150
    )

    plt.close(fig)  # Close the figure to free memory

    image_buffer.seek(0)

    # Convert PNG to base64
    image_base64 = base64.b64encode(
        image_buffer.getvalue()
    ).decode("utf-8")

    return jsonify({
        "teams": team_names_df.to_html(index=False),
        "image": image_base64
    })


if __name__ == "__main__":
    app.run(debug=True)