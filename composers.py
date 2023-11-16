from dataclasses import dataclass

@dataclass
class Composer:
	name: str
	dates: str
	n_pieces: int

	def __str__(self):
		res = self.name
		if len(self.dates):
			res += f" ({self.dates})"
		res += f" ({self.n_pieces})"
		return res


COMPOSERS = []

COMPOSER_DATES = {
	"Agostini, Lodovico": "1534-1590",
	"Agricola, Alexander": "1457?-1506",
	"Albano, Marcello": "?-1616*",
	"Alberti, Innocenzo": "1535-1615",
	"Anonymous": "",
	"Asola, Giammateo": "1524-1609",
	"Bacchini, Giovanni Maria": "",
	"Baccusi, Ippolito": "1550-1609",
	"Balsamino, Simone": "?-1600*",
	"Barbarino, Bartolomeo": "1568-1617",
	"Barra, Hotinet": "1490?-1523*",
	"Bauldeweyn, Noel": "1480?-1529",
	"Bellanda, Lodovico": "1575?-1613*",
	"Bellasio, Paolo": "1554-1594",
	"Bellaver, Vincenzo": "1540-1587",
	"Belli, Girolamo": "1552-1620?",
	"Belli, Giulio": "1560-1621",
	"Benedetti, Piero": "*1585-1649*",
	"Billi, Lucio": "1575?-1603*",
	"Binchois, Gilles": "1400?-1460",
	"Bisgueria": "",
	"Bonelli, Aurelio": "1569?-1620*",
	"Bonini, Pietro Andrea": "*1550-1605*",
	"Borelli, Francesco Maria": "",
	"Borsaro, Arcangelo": "1560?-1617",
	"Boschetti, Giovanni Boschetto": "1588-1622",
	"Bozi, Paolo": "1550?-1595",
	"Brumel, Antoine": "1460?-1512",
	"Busnoys, Antoine": "1430?-1492",
	"Busnoys, Antoine*": "1430?-1492",
	"Camarella, Giovanni Battista": "",
	"Cancineo, Michelangelo": "1550?-1608*",
	"Cantino, Paolo": "",
	"Capilupi, Geminiano": "1573-1616",
	"Caprioli, Giovanni Paolo": "1580?-1627?",
	"Cavatoni, Pietro": "",
	"Cerbello, Giovanni Battista": "",
	"Champion, Nicolas": "1475-1533",
	"Cifra, Antonio": "1584?-1629",
	"Cirullo, Giovanni Antonio": "?-1610*",
	"Civita, Davit": "",
	"Clemsee, Christoforo": "",
	"Coma, Annibale": "1543?-?",
	"Compere, Loyset": "1440?-1518",
	"Conseil, Jean": "1498?-1534",
	"Corfini, Jacopo": "1540?-1591",
	"Cortellini, Camillo": "1561-1630",
	"Dalla Casa, Girolamo": "?-1601",
	"Dalla Gostena, Giovanni Battista": "1540?-1598",
	"Daser, Ludwig": "1526?-1589",
	"De Castro, Jean": "1540?-1611",
	"De Fevin, Antoine": "1570?-1612",
	"De Hodemont, Leonard Collet": "1575-1636",
	"De Macque, Giovanni": "1549?-1614",
	"De Orto, Marbrianus": "1460?-1529",
	"De Orto, Marbrianus*": "1460?-1529",
	"De Sermisy, Claudin": "1490?-1562",
	"De Silva, Andreas": "1475?-1530?",
	"De Therache, Pierrequin": "1470?-1528",
	"De Wert, Giaches": "1535?-1596",
	"De la Fage, Jean": "",
	"De la Rue, Pierre": "1452-1518",
	"Del Mel, Rinaldo": "1554?-1598?",
	"Della Rota, Adriano": "",
	"Dentice, Scipione": "1560-1633",
	"Dering, Richard": "1580?-1630",
	"Des Prez, Josquin": "1450?-1521",
	"Des Prez, Josquin*": "1450?-1521",
	"Di Costanzo, Alessandro": "",
	"Di Monte, Filippo": "1521-1603",
	"Dindia, Sigismondo": "1582?-1629",
	"Dragoni, Giovanni Andrea": "1540-1598",
	"Du Fay, Guillaume": "1397?-1474",
	"Du Fay, Guillaume*": "1397?-1474",
	"Duc, Filippo": "1550?-1586*",
	"Dueto, Antonio": "1535?-1594*",
	"Effrem, Muzio": "1549-1640*",
	"Erasmus": "",
	"Eredi, Francesco": "1575?-?",
	"Eremita, Giulio": "1550?-1600?",
	"Feliciani, Andrea": "?-1596",
	"Felis, Stefano": "1538?-1603",
	"Ferrabosco, Alfonso": "1543-1588",
	"Ferro, Pier Matheo": "",
	"Festa, Costanzo": "1485?-1545",
	"Festa, Sebastiano": "1490?-1524",
	"Fonghetti, Paolo": "1572-*1630",
	"Fontanelli, Alfonso": "1557-1622",
	"Fornaci, Giacomo": "",
	"Frye, Walter": "?-1474?",
	"Gabella, Giovanni Battista": "1550?-1626*",
	"Gallo, Vincenzo": "1560-1624",
	"Garzi, Pietro Francesco": "1600?-1641",
	"Gastoldi, Giovanni Giacomo": "1555?-1609",
	"Genvino, Francesco": "1580?-*1633",
	"Gesualdo, Carlo": "1566-1613",
	"Gherardini, Arcangelo": "",
	"Ghizzolo, Giovanni": "1580?-1625?",
	"Giovannelli, Ruggiero": "1560?-1625",
	"Giramo, Pietro Antonio": "?-1630*",
	"Gombert, Nicholas": "1495-1560",
	"Guami, Francesco": "1554-1602",
	"Guami, Gioseffo": "1542-1612",
	"Guelfi, Antonio": "",
	"Hassler, Hans Leo": "1564-1612",
	"Hellinck, Lupus": "1493-1541",
	"Il Verso, Antonio": "1560?-1621",
	"Ingegneri, Marco Antonio": "1536-1592",
	"Isaac, Heinrich": "1450?-1517",
	"Isnardi, Paolo": "1536?-1596",
	"Jachet of Mantua": "1483-1559",
	"Jacotin": "",
	"Japart, Jean": "",
	"Lambardi, Francesco": "1587-1642",
	"Landi, Stefano": "1587-1639",
	"Le Santier, Jean": "",
	"Lheritier, Jean": "1480-1551*",
	"Lupi, Johannes": "1506?-1539",
	"Luzzaschi, Luzzasco": "1545-1607",
	"Macigni, Giovanni": "",
	"Maistre Jan": "1485?-1538",
	"Malcort, Abertijne*": "?-*1519",
	"Malpigli, Gentile": "",
	"Malvezzi, Christofano": "1547-1599",
	"Mancini, Curzio": "1553?-1611",
	"Marenzio, Luca": "1553-1599",
	"Martini, Johannes": "1440?-1497",
	"Martini, Johannes*": "1440?-1497",
	"Moulu, Pierre": "1484?-1550?",
	"Mouton, Jean": "1459?-1522",
	"Obrecht, Jacob": "1457?-1505",
	"Ockeghem, Johannes": "1430-1495",
	"Ockeghem, Johannes*": "1430-1495",
	"Palestrina, Giovanni Pierluigi da": "1525-1594",
	"Pipelare, Matthaeus": "1450?-1515?",
	"Regis, Johannes": "1425?-1496?",
	"Renaldo": "?-1512?",
	"Richafort, Jean": "1480?-1547?",
	"Tinctoris, Johannes": "1435?-1511",
	"Verdelot, Philippe": "1485?-1552?",
	"Vinders, Jheronimus": "1500?-1560?",
	"Willaert, Adrian": "1490-1562",
}

# TODO: Add dates for the following composers (coming from the Tasso music project)

"""Marini, Biagio
	Marotta, Erasmo
	
	Masnelli, Paolo
	Massaino, Tiburzio
	Mazza, Francesco
	Mazzocchi, Domenico
	Meldert, Leonardo
	Melli, Domenico Maria
	Merulo, Claudio
	Milleville, Alessandro
	Molinaro, Simone
	Montella, Giovan Domenico
	Monteverdi, Claudio
	
	Naldi, Romolo
	Nanino, Giovanni Bernardino
	Nantermi, Orazio
	Narducci, Benedetto
	Negri, Francesco
	Nenna, Pomponio
	Nielsen, Hans
	
	Pallavicino, Benedetto
	Person, Diego
	Philips, Peter
	
	Pordenon, Marco Antonio
	Porta, Costanzo
	Porto, Allegro
	Preti, Alfonso
	Priuli, Giovanni
	Raval, Sebastiano
	Recalchi, Giovanni Battista
	
	Ricci, Cesarina
	
	Roccia, Dattilo
	Roinci, Luigi
	Sabbatini, Vincenzo
	Salzilli, Crescenzio
	Santini, Marsilio
	Saracini, Claudio
	Scozzese, Agostino
	Serafico, Benedetto
	Spano, Donato Antonio
	Stefani, Giovanni
	Stivori, Francesco
	Striggio, Alessandro
	
	Torelli, Gaspare
	Torscianello, Enrico
	Tosone, Marcello
	Tresti, Flaminio
	Vecchi, Orazio
	Vecoli, Regolo
	Veggio, Giovanni Agostino
	
	Verdonck, Cornelis
	Vignali, Francesco
	Villani, Gabriele
	Vinci, Pietro
	
	Virchi, Paolo
	Vittori, Loreto
	
	Zanotti, Camillo
	Zenaro, Giulio
}"""