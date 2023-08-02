from typing import Union

def duplicate_headers(headers: list, min_col: int = 0) -> dict:
    """Returns a dictionary of duplicate field headers, where field
    headers appearing more than once in the headers list, they are keys
    and the corresponding list contains the indices of each instance of
    the duplicated header.

    Parameters
    ----------
    headers : list
        List of header to check for duplicates

    min_col : int (Optional)
        First position in the file
    
    Returns
    -------
    dict -> {<field_header: str>: [<field_position: int>]}
        Dictionary of field headers, and field header positions
        in the file.
    """
    has_duplicates = False
    for header in headers:
        if headers.count(header) > 1:
            has_duplicates = True
            break

    if has_duplicates is True:
        duplicates = {}
        for num, header in enumerate(headers):
            if header.count(header) > 1:
                if header in duplicates.keys():
                    duplicates[header].append(num + min_col)
                
                else:
                    duplicates[header] = [num + min_col]
        
        return duplicates
    
    return None
