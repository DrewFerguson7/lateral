"""Add well-known pre-1996 jersey numbers that the nflverse data lacks (it only has numbers from 1996 on).
Only signature numbers we are confident about; anything uncertain is left out. Idempotent."""
import pickle
NUMS = {
 'Randall Cunningham': [12], 'Walter Payton': [34], 'Jim Brown': [32], 'Dick Butkus': [51], 'Gale Sayers': [40], 'Jack Lambert': [58],
 'Jack Ham': [59], 'Joe Greene': [75], 'Lynn Swann': [88], 'John Stallworth': [82], 'Franco Harris': [32], 'Mel Blount': [47],
 'Mike Webster': [52], 'Earl Campbell': [34], 'Eric Dickerson': [29], 'O.J. Simpson': [32], 'Larry Csonka': [39], 'Paul Warfield': [42],
 'Dan Fouts': [14], 'Kellen Winslow (TE 1979)': [80], 'Steve Largent': [80], 'James Lofton': [80], 'Art Monk': [81], 'Charlie Joiner': [18],
 'Ozzie Newsome': [82], 'Howie Long': [75], 'Mike Singletary': [50], 'Dan Hampton': [99], 'Steve McMichael': [76], 'Jim Covert': [74],
 'Ray Nitschke': [66], 'Paul Hornung': [5], 'Jim Taylor (RB 1958)': [31], 'Forrest Gregg': [75], 'Herb Adderley': [26], 'Willie Wood': [24],
 'Willie Davis (DL 1958)': [87], 'Jerry Kramer': [64], 'Henry Jordan': [74], 'Raymond Berry': [82], 'Lenny Moore': [24], 'John Mackey': [88],
 'Jim Parker': [77], 'Gino Marchetti': [89], 'Art Donovan': [70], 'Deacon Jones': [75], 'Merlin Olsen': [74], 'Jack Youngblood': [85],
 'Jackie Slater': [78], 'Tom Mack': [65], 'Fred Biletnikoff': [25], 'Gene Upshaw': [63], 'Art Shell': [78], 'Ted Hendricks': [83],
 'Willie Brown (DB 1963)': [24], 'Cliff Branch': [21], 'George Blanda': [16], 'Ray Guy': [8], 'Lance Alworth': [19], 'Ron Mix': [74],
 'Don Maynard': [13], 'Winston Hill': [75], 'Joe Klecko': [73], 'Bob Lilly': [74], 'Mel Renfro': [20], 'Rayfield Wright': [70],
 'Drew Pearson': [88], 'Bob Hayes': [22], 'Cliff Harris': [43], 'Chuck Howley': [54], 'Lee Roy Selmon': [63], 'Sam Huff': [70],
 'Frank Gifford': [16], 'Y.A. Tittle': [14], 'Emlen Tunnell': [45], 'Rosey Brown': [79], 'Sonny Jurgensen': [9], 'Sammy Baugh': [33],
 'Charley Taylor': [42], 'Bobby Mitchell': [49], 'Russ Grimm': [68], 'John Riggins': [44], 'Chris Hanburger': [55], 'Ken Houston': [27],
 'Ken Riley': [13], 'Anthony Munoz': [78], 'Andre Tippett': [56], 'John Hannah': [73], 'Nick Buoniconti': [85], 'Larry Little': [66],
 'Jim Langer': [62], 'Dick LeBeau': [44], 'Lem Barney': [20], 'Alex Karras': [71], 'Joe Schmidt': [56], 'Doak Walker': [37],
 'Bobby Layne': [22], 'Yale Lary': [28], 'Charlie Sanders': [88], 'Leroy Kelly': [44], 'Gene Hickerson': [66], 'Marion Motley': [76],
 'Dante Lavelli': [86], 'Norm Van Brocklin': [11], 'Bob Waterfield': [7], 'Floyd Little': [44], 'Randy Gradishar': [53], 'Larry Wilson': [8],
 'Jackie Smith': [81], 'Dan Dierdorf': [72], 'Ollie Matson': [33], 'Hugh McElhenny': [39], 'Joe Perry': [34], 'Leo Nomellini': [73],
 'Bob St. Clair': [79], 'Jimmy Johnson': [37], 'Dave Wilcox': [64], 'Elvin Bethea': [65], 'Robert Brazile': [52], 'Mike Munchak': [63],
 'Buck Buchanan': [86], 'Bobby Bell (LB 1963)': [78], 'Willie Lanier': [63], 'Jan Stenerud': [3], 'Emmitt Thomas': [18],
 'Johnny Robinson (DB 1960)': [42], 'Curley Culp': [61], 'Kenny Easley': [45], 'Dave Casper': [87], 'Fred Dean (DL 1975)': [74],
 'Bronko Nagurski': [3], 'Sid Luckman': [42], 'Bulldog Turner': [66], 'Mike Ditka': [89], 'Bill George': [61], 'Doug Atkins': [81],
 'Sterling Sharpe': [84], 'Rickey Jackson': [57], 'Tommy McDonald': [25], 'Chuck Bednarik': [60], 'Harold Carmichael': [17],
 'Claude Humphrey': [87], 'Joe DeLamielleure': [68], 'Billy Shaw': [66], 'Jim Ringo': [51], 'Donnie Shell': [31], 'Ernie Stautner': [70],
 'John Henry Johnson': [35], 'Bobby Dillon': [44], 'Tony Canadeo': [3], 'Don Hutson': [14], 'Lou Creekmur': [76], 'Jack Christiansen': [24],
 'George Halas': [7], 'Mel Hein': [7],
}
P, TN = pickle.load(open('P3.pkl', 'rb'))
by = {}
for k, p in P.items(): by.setdefault(p['disp'], []).append(k)
added, missing = 0, []
for n, nums in NUMS.items():
    ks = [k for k in by.get(n, []) if P[k]['first'] < 1996]
    if len(ks) != 1: missing.append(n); continue
    p = P[ks[0]]
    for u in nums:
        if u not in p['nums']: p['nums'] = sorted(p['nums'] + [u]); added += 1
    if not p.get('main'): p['main'] = nums[0]
pickle.dump((P, TN), open('P3.pkl', 'wb'))
print('numbers added:', added, '| names not found:', missing)
