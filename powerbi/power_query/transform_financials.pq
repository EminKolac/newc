// Power Query: Transform Bloomberg FA Export (Wide to Long)
let
    Source = Excel.Workbook(File.Contents("Bloomberg_FA_Export.xlsx"), null, true),
    IS_TRY_Raw = Source{[Item="Cash Flow - Standardized",Kind="Sheet"]}[Data],
    IS_TRY_Headers = Table.PromoteHeaders(IS_TRY_Raw, [PromoteAllScalars=true]),
    IS_TRY_Unpivoted = Table.UnpivotOtherColumns(IS_TRY_Headers, {"Item"}, "Quarter_Raw", "Value"),
    IS_TRY_Cleaned = Table.TransformColumns(IS_TRY_Unpivoted, {{"Value", each if _ = "\u2014" or _ = "" then null else Number.From(_), type number}}),
    IS_TRY_WithDate = Table.AddColumn(IS_TRY_Cleaned, "Q_Date", each Date.From([Quarter_Raw]), type date),
    IS_TRY_WithCurrency = Table.AddColumn(IS_TRY_WithDate, "Currency", each "TRY", type text),
    IS_USD_Raw = Source{[Item="BBG Adjusted",Kind="Sheet"]}[Data],
    IS_USD_Headers = Table.PromoteHeaders(IS_USD_Raw, [PromoteAllScalars=true]),
    IS_USD_Unpivoted = Table.UnpivotOtherColumns(IS_USD_Headers, {"Item"}, "Quarter_Raw", "Value"),
    IS_USD_Cleaned = Table.TransformColumns(IS_USD_Unpivoted, {{"Value", each if _ = "\u2014" or _ = "" then null else Number.From(_), type number}}),
    IS_USD_WithDate = Table.AddColumn(IS_USD_Cleaned, "Q_Date", each Date.From([Quarter_Raw]), type date),
    IS_USD_WithCurrency = Table.AddColumn(IS_USD_WithDate, "Currency", each "USD", type text),
    Combined = Table.Combine({IS_TRY_WithCurrency, IS_USD_WithCurrency}),
    Pivoted = Table.Pivot(Combined, List.Distinct(Combined[Item]), "Item", "Value"),
    #"Added Q_Label" = Table.AddColumn(Pivoted, "Q_Label", each Text.From(Date.Year([Q_Date])) & "-Q" & Text.From(Date.QuarterOfYear([Q_Date])), type text),
    #"Added Sort_Order" = Table.AddColumn(#"Added Q_Label", "Sort_Order", each Date.Year([Q_Date]) * 10 + Date.QuarterOfYear([Q_Date]), Int64.Type)
in
    #"Added Sort_Order"
