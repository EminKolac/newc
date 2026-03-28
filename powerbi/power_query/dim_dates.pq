// Power Query: dim_Dates (Q1 2015 to Q4 2030)
let
    StartDate = #date(2015, 1, 1),
    EndDate = #date(2030, 12, 31),
    QuarterEnds = List.Select(
        List.Dates(StartDate, Duration.Days(EndDate - StartDate), #duration(1,0,0,0)),
        each Date.Day(Date.EndOfMonth(_)) = Date.Day(_) and List.Contains({3,6,9,12}, Date.Month(_))
    ),
    #"To Table" = Table.FromList(QuarterEnds, Splitter.SplitByNothing(), {"Quarter_Date"}),
    #"Changed Type" = Table.TransformColumnTypes(#"To Table", {{"Quarter_Date", type date}}),
    #"Added Year" = Table.AddColumn(#"Changed Type", "Year", each Date.Year([Quarter_Date]), Int64.Type),
    #"Added Quarter_Num" = Table.AddColumn(#"Added Year", "Quarter_Num", each Date.QuarterOfYear([Quarter_Date]), Int64.Type),
    #"Added Quarter_Label" = Table.AddColumn(#"Added Quarter_Num", "Quarter_Label",
        each Text.From([Year]) & "-Q" & Text.From([Quarter_Num]), type text),
    #"Added Sort_Order" = Table.AddColumn(#"Added Quarter_Label", "Sort_Order",
        each [Year] * 10 + [Quarter_Num], Int64.Type),
    #"Added Quarters_From_Start" = Table.AddColumn(#"Added Sort_Order", "Quarters_From_Start",
        each (([Year] - 2015) * 4 + [Quarter_Num] - 1), Int64.Type)
in
    #"Added Quarters_From_Start"
