// Power Query: fact_Dividends
let
    Source = Excel.Workbook(File.Contents("BIST_Portfolio_V3.xlsx"), null, true),
    DivSheet = Source{[Item="fact_Dividends",Kind="Sheet"]}[Data],
    Headers = Table.PromoteHeaders(DivSheet, [PromoteAllScalars=true]),
    Typed = Table.TransformColumnTypes(Headers, {
        {"Ticker", type text}, {"Payment_Date", type date},
        {"Net_DPS_TRY", type number}, {"Net_DPS_USD", type number},
        {"Total_Cash_Dividend", type number}, {"Your_Dividend_Income", type number},
        {"Payout_Ratio", type number}
    }),
    #"Added Q_Date" = Table.AddColumn(Typed, "Q_Date", each Date.EndOfQuarter([Payment_Date]), type date),
    #"Added Q_Label" = Table.AddColumn(#"Added Q_Date", "Q_Label",
        each Text.From(Date.Year([Q_Date])) & "-Q" & Text.From(Date.QuarterOfYear([Q_Date])), type text)
in
    #"Added Q_Label"
