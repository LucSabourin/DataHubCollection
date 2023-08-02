function xlBreakLinks(strFileLocation)
    dim xl
    dim xlBook
    dim links
    dim counter

    xl = createobject("Excel.Application")
    Set xlBook = xl.workbooks.open(strFileLocation)

    links = xlBook.LinkSources(xlLinkTypeExcelLinks)

    if links = Empty then exit function

    for counter = 1 to ubound(links)
        xlBook.BreakLink links(i), xlLinkTypeExcelLinks
    next
end function
