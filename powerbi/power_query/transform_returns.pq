// Power Query: Transform Bloomberg BDH Price Data -> fact_Returns
let
    Source = Excel.Workbook(File.Contents("Bloomberg_BDH_Prices.xlsx"), null, true),
    PriceSheet = Source{[Item="Prices",Kind="Sheet"]}[Data],
    Headers = Table.PromoteHeaders(PriceSheet, [PromoteAllScalars=true]),
    Unpivoted = Table.UnpivotOtherColumns(Headers, {"Date"}, "Ticker", "Price_Close"),
    Typed = Table.TransformColumnTypes(Unpivoted, {{"Date", type date}, {"Price_Close", type number}}),
    #"Added Quarter" = Table.AddColumn(Typed, "Q_Date", each Date.EndOfQuarter([Date]), type date),
    Grouped = Table.Group(#"Added Quarter", {"Ticker", "Q_Date"}, {{"Price_Close", each List.Last(List.Sort([Price_Close])), type number}}),
    #"Added Q_Label" = Table.AddColumn(Grouped, "Q_Label", each Text.From(Date.Year([Q_Date])) & "-Q" & Text.From(Date.QuarterOfYear([Q_Date])), type text),
    #"Added Sort_Order" = Table.AddColumn(#"Added Q_Label", "Sort_Order", each Date.Year([Q_Date]) * 10 + Date.QuarterOfYear([Q_Date]), Int64.Type)
in
    #"Added Sort_Order"
