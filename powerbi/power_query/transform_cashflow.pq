// Power Query: Transform Bloomberg Cash Flow Export (Wide to Long)
let
    Source = Excel.Workbook(File.Contents("Bloomberg_FA_Export.xlsx"), null, true),
    CF_TRY_Raw = Source{[Item="Cash Flow - Standardized (2)",Kind="Sheet"]}[Data],
    CF_TRY_Headers = Table.PromoteHeaders(CF_TRY_Raw, [PromoteAllScalars=true]),
    CF_TRY_Unpivoted = Table.UnpivotOtherColumns(CF_TRY_Headers, {"Item"}, "Quarter_Raw", "Value"),
    CF_TRY_Cleaned = Table.TransformColumns(CF_TRY_Unpivoted, {{"Value", each if _ = "\u2014" or _ = "" then null else Number.From(_), type number}}),
    CF_TRY_WithDate = Table.AddColumn(CF_TRY_Cleaned, "Q_Date", each Date.From([Quarter_Raw]), type date),
    CF_TRY_WithCurrency = Table.AddColumn(CF_TRY_WithDate, "Currency", each "TRY", type text),
    CF_USD_Raw = Source{[Item="Cash Flow - Standardized (2 (3))",Kind="Sheet"]}[Data],
    CF_USD_Headers = Table.PromoteHeaders(CF_USD_Raw, [PromoteAllScalars=true]),
    CF_USD_Unpivoted = Table.UnpivotOtherColumns(CF_USD_Headers, {"Item"}, "Quarter_Raw", "Value"),
    CF_USD_Cleaned = Table.TransformColumns(CF_USD_Unpivoted, {{"Value", each if _ = "\u2014" or _ = "" then null else Number.From(_), type number}}),
    CF_USD_WithDate = Table.AddColumn(CF_USD_Cleaned, "Q_Date", each Date.From([Quarter_Raw]), type date),
    CF_USD_WithCurrency = Table.AddColumn(CF_USD_WithDate, "Currency", each "USD", type text),
    Combined = Table.Combine({CF_TRY_WithCurrency, CF_USD_WithCurrency}),
    Pivoted = Table.Pivot(Combined, List.Distinct(Combined[Item]), "Item", "Value"),
    #"Added Q_Label" = Table.AddColumn(Pivoted, "Q_Label", each Text.From(Date.Year([Q_Date])) & "-Q" & Text.From(Date.QuarterOfYear([Q_Date])), type text),
    #"Added Sort_Order" = Table.AddColumn(#"Added Q_Label", "Sort_Order", each Date.Year([Q_Date]) * 10 + Date.QuarterOfYear([Q_Date]), Int64.Type)
in
    #"Added Sort_Order"
