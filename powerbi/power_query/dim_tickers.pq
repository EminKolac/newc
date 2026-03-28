// Power Query: dim_Tickers
let
    Source = Excel.Workbook(File.Contents("BIST_Portfolio_V3.xlsx"), null, true),
    dim_Tickers = Source{[Item="dim_Tickers",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(dim_Tickers, [PromoteAllScalars=true]),
    #"Changed Types" = Table.TransformColumnTypes(#"Promoted Headers", {
        {"Ticker", type text}, {"Company_Name", type text}, {"Sector", type text},
        {"Ownership_Pct", type number}, {"Acq_Date", type date},
        {"Acq_Price_TRY", type number}, {"Acq_Price_USD", type number},
        {"Current_Price_TRY", type number}, {"Current_Price_USD", type number},
        {"Shares_Outstanding_M", type number}, {"Your_Value_TRY", type number},
        {"Your_Value_USD", type number}, {"Total_Return_TRY", type number},
        {"Total_Return_USD", type number}, {"CAGR_USD", type number}, {"IRR_USD", type number}
    })
in
    #"Changed Types"
