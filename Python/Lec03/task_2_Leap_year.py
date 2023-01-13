# Function to determine if the year is leap or not depends on three conditions
def is_leap(y):
    if y % 4 == 0:
        if y % 100 != 0 or y % 400 == 0:
            return True
        else:
            return False
    else:
        return False


# Function to test leap function
def test_leap():
    # Leap_years are the test cases (ideal results)
    leap_years = [1584, 1588, 1592, 1596, 1600, 1604, 1608, 1612, 1616, 1620, 1624, 1628, 1632, 1636, 1640, 1644, 1648,1652, 1656, 1660, 1664, 1668, 1672, 1676, 1680, 1684, 1688, 1692, 1696, 1704, 1708, 1712, 1716, 1720,1724, 1728, 1732, 1736, 1740, 1744, 1748, 1752, 1756, 1760, 1764, 1768, 1772, 1776, 1780, 1784, 1788,1792, 1796, 1804, 1808, 1812, 1816, 1820, 1824, 1828, 1832, 1836, 1840, 1844, 1848, 1852, 1856, 1860,1864, 1868, 1872, 1876, 1880, 1884, 1888, 1892, 1896, 1904, 1908, 1912, 1916, 1920, 1924, 1928, 1932,1936, 1940, 1944, 1948, 1952, 1956, 1960, 1964, 1968, 1972, 1976, 1980, 1984, 1988, 1992, 1996, 2000,2004, 2008, 2012, 2016, 2020]
    test_results = []
    # Adding the output of is_leap function in test_results
    for i in range(1584, 2021):
        if is_leap(i) == True:
            test_results.append(i)
    # Comparing our results with the ideal results
    print(test_results)
    if test_results == leap_years:
        print('Test succeeded')
    else:
        print("logic function is wrong revise it")

x = input("Enter Year:")
print(is_leap(int(x)))
