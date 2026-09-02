# Credit Risk Scorer

A Python tool that reads company financials, works out whether each company can afford
its debt, and grades it from AAA down to B.

![Credit risk scores by company](output/risk_chart.png)

## Why I built it

I spent a week on a work experience programme at Fitch Group, where I researched and
presented on how credit ratings work. Fitch assesses whether a company can repay its
debts and grades it from AAA down to D, and a downgrade makes it harder and more
expensive for that company to borrow.

I didn't want to just explain how ratings work, so I built a simplified version of the
assessment in code. Writing down the scoring criteria meant deciding what actually makes
a company risky and how much each factor should count. That turned out to be a judgement
call rather than a formula.

This is my first Python project. I study a BTEC in Engineering, which has no coding on it.

## What it does

It reads a CSV of company financials and calculates four ratios:

- **Interest cover** — operating profit divided by the annual interest bill. How many
  times over the company's earnings cover what it owes its lenders
- **Net debt to profit** — debt minus cash, divided by profit. Roughly how many years of
  profit it would take to clear the debt
- **Operating margin** — how much profit the company keeps from each pound of sales
- **Debt to equity** — how much is borrowed against what the owners put in

Each ratio scores 1 to 5 against threshold bands. The scores combine into one weighted
number, which becomes a rating band.

Interest cover and net debt count 30% each; margin and gearing 20% each. I weighted it
that way because the first two answer whether the company can afford what it owes, and
the other two only describe the business.

## Running it

```bash
pip install pandas matplotlib
python3 score.py
```

## Output

```
CREDIT RISK SCORECARD
==============================================================================
                company  interest_cover  net_debt_to_profit  operating_margin  total_score grade
   Example Software plc           53.75               -1.95              0.24          5.0   AAA
     Example Retail plc            4.84                3.97              0.07          3.2   BBB
  Example Utilities plc            3.05                7.38              0.21          2.6    BB
Example Industrials plc            1.64               10.47              0.07          1.9     B
   Example Airlines plc            1.23               14.54              0.04          1.2     B
==============================================================================
```

The software company's net debt is negative because it holds more cash than debt, so
there is nothing for it to struggle to repay. The airline covers its interest bill only
1.23 times, so one bad year and it can't pay.

## The data

`data/companies.csv` holds example figures, not real companies. To run it on real
businesses, replace the rows with published figures from annual reports.

Columns needed, all in millions:
`company, revenue_m, operating_profit_m, total_debt_m, cash_m, interest_expense_m, equity_m`

## What I'd change next

The thresholds should really vary by sector. A utility with regulated income can carry
much more debt than an airline, but at the moment both are judged against the same bars.
I'd also want to track a company's score across several years, since a rating is reviewed
over time rather than set once.
