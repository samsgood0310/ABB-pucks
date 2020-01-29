# ABB-pucks
Complete code for localizing and picking pucks with an IRB 140 robot arm. Image processing in Python and Rest API to communicate between Python and RobotWare.

class RAPID;

**__init__:**  
Initializes base url, username and password


**def set_rapid_variable:**   
POSR request to update variables in RAPID
Requires name of variable and value
returns nothing

**def get_rapid_variable:**  
GET request to gather value from variable in RAPID
Requires name of variable
returns the value of the specified variable

**set_robtarget_variables:** 
Calls on the function **set_rapid_variable**, manipulated to be able to update robtargets
Requires name of variable and \[x, y, z\]
Kaller på funksjonen *set_rapid_variable*, manipulert til å kunne oppdatere robtargets
Krever variabelnavn og [x,y,z] koordinater
returnerer ingenting


**get_robtarget_variables:** 

GET request for å hente ut verdien til robtarget i RAPID
Krever variabelnavn
returnerer translasjon[x,y,z] og rotasjon[C, X*S, Y*S, Z*S]


**set_offset_variables:**

Kaller på funksjonen *set_rapid_variable*, manipulert til å kunne oppdatere en offset array
Krever variabelnavn og [x,y] array.
returnerer ingenting


**wait_for_rapid:**
Kaller på funksjonen *get_rapid_variable* for å hente 'ready_flag' variabel
'ready_flag' sjekkes på i en while løkke med et satt intervall
'ready_flag' settes til FALSE igjen når sjekken er ferdig
returnerer ingenting


'''' PROGRAMMET SKAL FUNGERE SOM FØLGER '''' (**Midlertidig**)

En session blir laget
- test = RAPID()

Initialiserer nødvendige variabler:
- angles array
- positions array
- table_height
- WRD ('what RAPID does')


En evig løkke rundt hovedprogrammet, slik at vi slipper å kjøre programmet om igjen og om igjen

# TODO: !!! Lage en GUI som fungerer omtrent på samme måte som if-løkken nedenfor ( ikke spesielt viktig, men kanskje noe å jobbe med til slutt)


	while løkke som venter på RAPID

	**** endringer må gjøres her **** (kanskje få til at du kan velge [x,y] koordinat som du ønsker at pucken skal flyttes til, eller at stacken skal flyttes til

	- brukeren får flere valgmuligheter om hva som ønskes at skal gjøres
		1. Bilde ovenfra (må gjøres først for å finne puckene)
		2. Flytt puck til midten
		3. Stack pucker
		4. Roter puck
		5. Avslutt

	- en if-løkke brukes for å kjøre det som blir valgt av brukeren
	
	valg 1:
	- setter WPW (what Python wants) til 1 -> kjører da CASE 1 i RAPID
	- kjører *wait_for_rapid* funksjonen slik at kamera kommer i posisjon
	- **** ta bilde og scanne qr-koder
	- hente ut [x, y] posisjoner (allerede konvertert til mm i selve QR-skanneren)
	- hente ut vinkler
	- kalkulere hvor mange klosser (pucker) som er på bordet
	- legge til en "table_height" i [x,y] posisjonene slik at de kan brukes til å oppdatere robtarget
	- oppdaterer så en array med robtargets med alle nåværende posisjoner
	- oppdaterer også en array med alle vinkler

	valg 2:
	- brukeren blir spurt om hvilken av klossene (puckene) som skal bli flyttet til midten
	- avhengig av hvilken puck som velges oppdateres robtarget til posisjon til valgt puck
	- dette gjelder også for vinkelen til klossen (pucken) som også blir oppdatert
	- alt er nå oppdatert og klart til å kjøre, så WPW (what Python wants) blir oppdatert til 2. -> kjører da CASE 2 i RAPID
	- kjører *wait_for_rapid* funksjonen slik at kamera kommer i posisjon
	- ta nytt bilde og scanne for qr-kode (nå mer presist for vi er nærmere klossen)
	- **** på en eller annen måte finne nye hvor mye vi må 'offsete'(forskyve) de allerede lagt inn koordinatene for å treffe klossen mer presist
	- **** vinkelen kan også oppdateres, men regner med den er ganske presis fra forrige utregning
	- **** oppdatere "offset" arrayen, og bruk denne for å forskyve det allerede konstruerte robtargetet
	- sender et image_processed:=TRUE inn til RAPID for å forsikre at prossesseringen av bilde blir ferdig før vi kjører videre i RAPID programmet

	valg 3:
	- oppdaterer variablene numberOfPucks, i og med at denne brukes i stackPucks funksjonen i RAPID.
	- setter WPW (what Python wants) til 3 -> kjører da CASE 3 i RAPID
	- funksjonen "stackPucks()" i RAPID må vente hver gang vi skal ta nytt bilde i *safe_position* over klossen (pucken)
	- ta nytt bilde og scanne for qr-kode (nå mer presist for vi er nærmere klossen)
	- **** på en eller annen måte finne nye hvor mye vi må 'offsete'(forskyve) de allerede lagt inn koordinatene for å treffe klossen mer presist
	- **** vinkelen kan også oppdateres, men regner med den er ganske presis fra forrige utregning
	- **** oppdatere "offset" arrayen, og bruk denne for å forskyve det allerede konstruerte robtargetet
	- sender et image_processed:=TRUE inn til RAPID for å forsikre at prossesseringen av bilde blir ferdig før vi kjører videre i RAPID programmet
	- funksjonen skal så plukke opp den spesifikke pucken og plassere den i midten.
	- dette gjentas for hver puck som er identifisert


# TODO: !!! lage en funksjon som: (bilde-prossesserings funksjon)
	- tar bilde
	- på en eller annen måte finne nye hvor mye vi må 'offsete'(forskyve) de allerede lagt inn koordinatene for å treffe klossen mer presist
	- vinkelen kan også oppdateres, men regner med den er ganske presis fra forrige utregning
	- oppdatere "offset" arrayen, og bruk denne for å forskyve det allerede konstruerte robtargetet
	- sender et image_processed:=TRUE inn til RAPID for å forsikre at prossesseringen av bilde blir ferdig før vi kjører videre i RAPID programmet

# TODO: !!! lage en funksjon som: ("init" bilde og posisjoner funksjon)
	- tar bilde og scanner qr-koder
	- henter ut [x,y] posisjoner og legger til en "table_height
