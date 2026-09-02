"""
Scores companies on how safely they can carry their debt, and gives each one a
grade from AAA down to B. A simplified version of what a credit ratings agency does.

Run it with: python3 score.py
"""

import pandas as pd
import matplotlib
matplotlib.use("Agg")   # save charts to a file instead of opening a window
import matplotlib.pyplot as plt


def load_companies(path="data/companies.csv"):
    return pd.read_csv(path)


def add_ratios(df):
    # take the cash off first. if you hold more cash than debt you are not really in debt
    df["net_debt_m"] = df["total_debt_m"] - df["cash_m"]
    df["interest_cover"] = df["operating_profit_m"] / df["interest_expense_m"]
    df["net_debt_to_profit"] = df["net_debt_m"] / df["operating_profit_m"]
    df["operating_margin"] = df["operating_profit_m"] / df["revenue_m"]
    df["debt_to_equity"] = df["total_debt_m"] / df["equity_m"]
    return df


def band_score(value, thresholds, higher_is_better):
    """Turn a ratio into a score from 1 (weakest) to 5 (strongest)."""
    if pd.isna(value):
        return 1
    # check the bars from best to worst and stop at the first one cleared
    for score, cut in zip([5, 4, 3, 2], thresholds):
        if (higher_is_better and value >= cut) or (not higher_is_better and value <= cut):
            return score
    return 1


def score_companies(df):
    # i picked these bands myself. 8 times cover looked comfortable, under 1.5 looked like trouble
    df["s_interest_cover"] = df["interest_cover"].apply(
        band_score, thresholds=[8, 5, 3, 1.5], higher_is_better=True)
    df["s_net_debt"] = df["net_debt_to_profit"].apply(
        band_score, thresholds=[1, 2.5, 4, 6], higher_is_better=False)
    df["s_margin"] = df["operating_margin"].apply(
        band_score, thresholds=[0.20, 0.12, 0.07, 0.03], higher_is_better=True)
    df["s_gearing"] = df["debt_to_equity"].apply(
        band_score, thresholds=[0.5, 1.0, 1.75, 2.5], higher_is_better=False)

    # interest cover and net debt count more because they show whether the company can pay.
    # margin and gearing only describe the business, they dont tell you about repaying
    df["total_score"] = (
        df["s_interest_cover"] * 0.30
        + df["s_net_debt"] * 0.30
        + df["s_margin"] * 0.20
        + df["s_gearing"] * 0.20
    ).round(2)
    return df


def to_grade(score):
    if score >= 4.5:
        return "AAA"
    if score >= 4.0:
        return "AA"
    if score >= 3.5:
        return "A"
    if score >= 2.8:
        return "BBB"
    if score >= 2.0:
        return "BB"
    return "B"


def make_chart(df, path="output/risk_chart.png"):
    ordered = df.sort_values("total_score")
    colours = ["#c0392b" if s < 2.8 else "#e67e22" if s < 3.5 else "#27ae60"
               for s in ordered["total_score"]]

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.barh(ordered["company"], ordered["total_score"], color=colours)
    ax.set_xlabel("Credit score (1 = weakest, 5 = strongest)")
    ax.set_title("Credit risk score by company")
    ax.set_xlim(0, 5)
    for y, (score, grade) in enumerate(zip(ordered["total_score"], ordered["grade"])):
        ax.text(score + 0.08, y, grade, va="center", fontsize=9)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    print(f"Chart saved to {path}")


def main():
    df = load_companies()
    df = add_ratios(df)
    df = score_companies(df)
    df["grade"] = df["total_score"].apply(to_grade)
    df = df.sort_values("total_score", ascending=False)

    report = df[["company", "interest_cover", "net_debt_to_profit",
                 "operating_margin", "total_score", "grade"]].round(2)

    print("\nCREDIT RISK SCORECARD")
    print("=" * 78)
    print(report.to_string(index=False))
    print("=" * 78)
    print(f"\nStrongest: {df.iloc[0]['company']} ({df.iloc[0]['grade']})")
    print(f"Weakest:   {df.iloc[-1]['company']} ({df.iloc[-1]['grade']})\n")

    df.to_csv("output/scores.csv", index=False)
    print("Full results saved to output/scores.csv")
    make_chart(df)


if __name__ == "__main__":
    main()
