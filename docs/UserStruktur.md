# User strukturen på sidan

Detta dokument skall beskriva user strukturen på sidan och hur det är tänkt att fungera rent tekniskt.

I grunden så har django redan en färdig lösning för User och group/permission hantering i django och då behöver man inte göra allt för mycket för att få det att fungera.

Men vi kommer iaf att alltid ha en vanlig django user i botten på allting. Sen så kommer vi ha x2 andra modeller implementerade, Trainer & Student.

Dessa 2 modeller kommer ha en OneToOne relation till User objektet och det gör att när man har ett request objekt i någon view metod i django så har man tillgång till 2 variablar `student` & `training` vilket kan användas för att avgöra vilken typ en användare är. Denna typ kontroll kan implementeras i hjälp decorators så att man kan skydda hela metoder så att endast en viss typ av users kan utföra en viss funktion.
