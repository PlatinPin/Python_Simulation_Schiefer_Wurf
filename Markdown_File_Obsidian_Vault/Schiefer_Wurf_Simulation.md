# <u>Simulation Schiefer Wurf in Python</u>

![[Default_Projectile_motion_Ball_2-removebg-preview.png]]
- [Einleitung](#Einleitung)
- [Code Erläuterungen](#Code%20Erläuterungen)
	- [Klassenvariablen](#Klassenvariablen)
	- [Konstruktor](#Konstruktor)
		- [Berechnung wann der Ball auf den Boden aufkommt](#Berechnung%20wann%20der%20Ball%20auf%20den%20Boden%20aufkommt)
		- [Berechnung wann der Ball am höchsten Punkt ankommt](#Berechnung%20wann%20der%20Ball%20am%20höchsten%20Punkt%20ankommt)
	- [Achsenbeschränbkungen des Wurfs](#Achsenbeschränbkungen%20des%20Wurfs)
	- [Berechnung der Wurf Parabel](#Berechnung%20der%20Wurf%20Parabel)
	- [Berechnung des Geschwindigkeitsvektors in y-Richtung](#Berechnung%20des%20Geschwindigkeitsvektors%20in%20y-Richtung)
	- [Berechung des Geschwindigkeitsvektors in x-richtung](#Berechung%20des%20Geschwindigkeitsvektors%20in%20x-richtung)
	- [Berechnung des Resultierendengeschwindigkeitsvektors](#Berechnung%20des%20Resultierendengeschwindigkeitsvektors)
	- [Berechnung der Kenetischen Energie](#Berechnung%20der%20Kenetischen%20Energie)
	- [Bestimmung des Startwertes und Achsenbeschränkungen der Kenetischen Energie](#Bestimmung%20des%20Startwertes%20und%20Achsenbeschränkungen%20der%20Kenetischen%20Energie)
	- [Berechnung der Potenziellen Energie](#Berechnung%20der%20Potenziellen%20Energie)
	- [Berechung des Statwertes und Achsenbeschränkungen der Potenziellen Energie](#Berechung%20des%20Statwertes%20und%20Achsenbeschränkungen%20der%20Potenziellen%20Energie)
	- [Erstellung der Animation](#Erstellung%20der%20Animation)
	- [Plot erstellen](#Plot%20erstellen)
		- [Wurf-Plot](#Wurf-Plot)
			- [Geschwindigkeitsvektoren](#Geschwindigkeitsvektoren)
		- [Kenetische Energie Plot](#Kenetische%20Energie%20Plot)
		- [Potenzielle Energie Plot](#Potenzielle%20Energie%20Plot)
		- [Plot für die Textfelder](#Plot%20für%20die%20Textfelder)
			- [Textfelder für die Energien](#Textfelder%20für%20die%20Energien)
			- [Textfelder für den Wurf](#Textfelder%20für%20den%20Wurf)
		- [Animation ausführen](#Animation%20ausführen)
	- [Hinzufügen der Pause/start Buttons](#Hinzufügen%20der%20Pause/start%20Buttons)

## Einleitung

In der folgenden Dokumentation wird ein Wurf mit einem Objekt, wie beispielsweise einem Ball, näherungsweise beschrieben. Dabei werden alle relevanten physikalischen Einflüsse auf den Wurf analysiert und entsprechend abgeleitet. Anschließend wird der Wurf mithilfe einer Simulation in der Programmiersprache Python umgesetzt. Hierbei kommen die Bibliotheken Matplotlib und NumPy zum Einsatz.

Diese Simulation zielt darauf ab, die Flugbahn eines Balls unter Berücksichtigung von Anfangsgeschwindigkeit und Abwurfwinkel zu approximieren. Dabei werden Fragen beantwortet wie die Flugweite, maximale Höhe, resultierende Geschwindigkeit sowie kinetische und potenzielle Energie des Objekts.

Innerhalb des Programmcodes können Parameter wie der Abwurfwinkel, die Anfangsgeschwindigkeit, die Masse des Objekts und die Abwurfhöhe variabel eingestellt werden. Das grafische Interface ermöglicht zudem das Pausieren der Simulation.

## Code Erläuterungen

Für die Simulation des Wurfs wurde eine Klasse namens "Wurf" entwickelt, welche alle relevanten Größen berechnet und verwaltet. Diese Klasse bietet eine strukturierte und effiziente Möglichkeit, die physikalischen Aspekte des Wurfs zu modellieren und zu untersuchen.

### Klassenvariablen

Für die Klassenvariablen wurden folgende Konstanten gewählt: Die Erdbeschleunigung g mit $9,81 \frac{m}{s^2}$, das Intervall, das angibt, wie viele Millisekunden zwischen zwei Bildern der Animation liegen sollen, und die Anzahl an Berechnungspunkten nn. Dies wurde so festgelegt, damit der Benutzer diese Konstanten nicht eigenständig beeinflussen kann.

```python
class wurf():
    g = 9.81
    inervall = 6
    n = 300
```

### Konstruktor

Im Konstruktor werden die Variablen für den Abwurfwinkel, die Abwurfgeschwindigkeit, die Masse des Objektes und die Abwurfhöhe festgelegt. Darüber hinaus werden die Geschwindigkeitskomponenten in x- und y-Richtung berechnet.

```python
    def __init__(self, a0_neu, v0_neu, m_neu, h_start_neu):
        self.a0 = np.radians(a0_neu)
        self.v0 = v0_neu
        self.m = m_neu
        self.h_start = h_start_neu
        self.vx0 = np.sin(self.a0) * self.v0
        self.vy0 = np.cos(self.a0) * self.v0
```

#### Berechnung wann der Ball auf den Boden aufkommt
Im Konstruktor wird zusätzlich berechnet, zu welchem Zeitpunkt das Objekt den Boden erreicht. Dies erfolgt durch die Anwendung der im ersten Kapitel hergeleiteten Gleichung für die Höhe, die auf Null gesetzt wird, um die Nullstellen dieses Polynoms zu bestimmen.

In Python wird dies mithilfe der Numpy-Funktion poly1d umgesetzt, gefolgt von der Verwendung von np.roots zur Berechnung der Nullstellen des Polynoms.

```python
# Berechnung des Zeitpunktes, bis der Ball auf den Boden kommt
coeff = [(-1)*(1/2)*self.g, self.vy0, self.h_start]
h1 = np.poly1d(coeff)
self.tstop = np.roots(h1)
```

#### Berechnung wann der Ball am höchsten Punkt ankommt
Im Konstruktor wird ebenfalls festgelegt, wann das Objekt den höchsten Punkt erreicht. Hierzu wird die zuvor hergeleitete Gleichung für die Höhe einmal abgeleitet und anschließend die Nullstellen berechnet.

Für diese Aufgabe wird erneut Numpy verwendet. Zur Ableitung eines Polynoms in Numpy wird die Funktion np.polyder(Funktion, m=1) verwendet, wobei m die Ordnung der Ableitung angibt.

```python
# Berechnung des Zeitpunktes, bis der Ball die maximale Höhe 
# erreicht hat
h1_ab1 = np.polyder(coeff, m=1)
self.t_hmax = np.roots(h1_ab1)
```


### Achsenbeschränbkungen des Wurfs

Um die Achsenbeschränkungen für das Koordinatensystem des Wurfs zu berechnen, benötigt man sowohl die maximale Strecke als auch die maximale Höhe, die der Ball erreicht.

Die maximale Strecke wird mithilfe der Formel für gleichförmige Bewegung bestimmt, indem man für die Zeit tt die berechnete Zeit einsetzt, zu der der Ball den Boden erreicht.

Die maximale Höhe wird erreicht, wenn die vertikale Geschwindigkeit, die in Richtung Erde wirkt, genau so groß ist wie die anfängliche vertikale Geschwindigkeitskomponente des Balls $v_{y0} = v_{a0}$​. Dies ergibt sich aus dem Gesetz für gleichmäßig beschleunigte Bewegungen:

$t = \frac{v_{y0}}{g}$

Dieser Zusammenhang, eingesetzt in die Berechnungsgleichung f¨ur die H¨ohe,
ergibt:

h = $v_{y0} \cdot (\frac{v_{y0}}{g} - \frac{1}{2} \cdot g \cdot (\frac{v_{y0}}{g})^2) + h_{start}$

```python
def achsen_ber(self):
	sxmax = self.vx0 * self.tstop[0]
	hmax = self.vy0 * (self.vy0/self.g) - (1/2) * self.g *
          (self.vy0/self.g)**2 + self.h_start
	return sxmax, hmax
```

### Berechnung der Wurf Parabel

Um die Flugbahn des Objekts zu berechnen, werden die Gleichungen für die Höhe h und die Strecke sx​ aus dem ersten Kapitel verwendet.

```python
def wurf_berechnung(self, t):
	h = self.vy0 * (t) - (1/2) * self.g * (t)**2 + self.h_start
	sx = self.vx0 * (t)
	return h, sx
```

### Berechnung des Geschwindigkeitsvektors in y-Richtung

Um den Vektor in vertikaler Richtung zu berechnen, wird zunächst der Betrag des Vektors ermittelt, wobei die entsprechende Formel bereits im vorherigen Kapitel hergeleitet wurde. Anschließend wird der Startpunkt des Vektors berechnet, der genau der Position entspricht, an der sich der Ball zum Zeitpunkt tt befindet. Dazu wird der Endpunkt des Vektors benötigt, der ebenfalls dem Betrag des Vektors entspricht, da der vertikale Vektor keine x-Koordinate besitzt. Daraufhin wird der Startwert mit dem Befehl "set offsets" aktualisiert und der Endpunkt mit "set UVC" aktualisiert.

```python
    def vek_ber_y(self, t):
        vy_vektor = self.vy0 - self.g*t
        v_start_y = self.vy0 * (t) - (1/2) * self.g * (t)**2 + self.h_start
        v_start_x = self.vx0 * t
        vy_ende_y = vy_vektor
        vy_ende_x = 0

        return v_start_y, v_start_x, vy_ende_y, vy_ende_x
```

### Berechung des Geschwindigkeitsvektors in x-richtung

Analog dazu wird mit dem Vektor in horizontaler Richtung verfahren:

```python
    def vek_ber_x(self, t):
        v_start_y = self.vy0 * (t) - (1/2) * self.g * (t)**2 + self.h_start
        v_start_x = self.vx0 * t
        v_ende_y = 0
        v_ende_x = self.vx0

        return v_start_y, v_start_x, v_ende_y, v_ende_x
```

### Berechnung des Resultierendengeschwindigkeitsvektors 

Für den resultierenden Geschwindigkeitsvektor wird analog wie zuvor verfahren. Zusätzlich wird der Betrag der resultierenden Geschwindigkeit berechnet und als Rückgabewert der Funktion übergeben.

```python
    def vek_ber_res(self, t):
        v_start_y = self.vy0 * (t) - (1/2) * self.g * (t)**2 + self.h_start
        v_start_x = self.vx0 * t
        vres_ende_x = self.vx0
        vres_ende_y = self.vy0 - self.g*t
        v_res = vres_ende_x + vres_ende_y

        return v_start_y, v_start_x, vres_ende_x, vres_ende_y, v_res
```

### Berechnung der Kenetischen Energie 

Um die kinetische Energie des Balls zu berechnen, wird die allgemeine Formel für kinetische Energie angewendet. Dabei werden für jeden neuen Zeitpunkt tt auch die Punkte aus der Vergangenheit berechnet, um einen kontinuierlich erweiterten Graphen zu erzeugen.

```python
    def Ekin_ber(self, t):
        x = np.linspace(0, t, int(25*t))
        V_res = np.sqrt((self.vx0)**2 + (self.vy0 - self.g*x)**2)
        Ekin = (1/2) * self.m * (V_res)**2
        Ekin_textfeld = (1/2) * self.m * (np.sqrt((self.vx0)**2 + (self.vy0 - self.g*t)**2))**2

        return Ekin, x, Ekin_textfeld
```

### Bestimmung des Startwertes und Achsenbeschränkungen der Kenetischen Energie

Um die kinetische Energie zum Startzeitpunkt zu berechnen, wird der Zeitpunkt t=0t=0 in die Gleichung für die kinetische Energie eingesetzt. Somit ist die maximale kinetische Energie auch zu Beginn vorhanden.

Die minimale kinetische Energie wird erreicht, wenn der Ball den Boden erreicht hat, da er ab diesem Zeitpunkt nicht mehr in Bewegung ist.

```python
    def Ekin_ber_achsen(self):
        Ekin_start = (1/2) * self.m * (self.vx0 + self.vy0)**2
        Ekin_min = (1/2) * self.m * (self.vx0 + (self.vy0 - self.g*self.tstop[0]))**2
        Ekin_max = Ekin_start
        
        return Ekin_start, Ekin_min, Ekin_max
```

### Berechnung der Potenziellen Energie

Analog dazu wird für die Potenziale Energie verfahren.

```python
    def Epot_ber(self, t):
        x = np.linspace(0, t, int(25*t))
        h = self.vy0 * (x) - (1/2) * self.g * (x)**2 + self.h_start
        Epot = (1/2) * self.m * h**2
        Epot_textfeld = (1/2) * self.m * (self.vy0 * (t) - (1/2) * self.g * (t)**2 + self.h_start)**2

        return x, Epot, Epot_textfeld
```

### Berechung des Statwertes und Achsenbeschränkungen der Potenziellen Energie

Analog zur Kentischen Energie:

```python
    def Epot_ber_achsen(self):
        h_max = self.vy0 * (self.t_hmax[0]) - (1/2) * self.g * (self.t_hmax[0])**2 + self.h_start
        Epot_max = (1/2) * self.m * (h_max)**2
        Epot_start = (1/2) * self.m * self.h_start
        
        return h_max, Epot_max, Epot_start
```

### Erstellung der Animation

Die Animationen werden alle durch eine Funktion gestartet und geupdatet.

```python
    def animate_wurf(self, t):

        h, sx = self.wurf_berechnung(t)
        ball.set_data(sx, h)

        v_start_y, v_start_x, vy_ende_y, vy_ende_x = self.vek_ber_y(t)
        vecy.set_offsets([v_start_x, v_start_y])
        vecy.set_UVC(vy_ende_x, vy_ende_y)

        v_start_y, v_start_x, v_ende_y, v_ende_x = self.vek_ber_x(t)
        vecx.set_offsets([v_start_x, v_start_y])
        vecx.set_UVC(v_ende_x, v_ende_y)

        v_start_y, v_start_x, vres_ende_x, vres_ende_y, v_res = self.vek_ber_res(t)
        vecres.set_offsets([v_start_x, v_start_y])
        vecres.set_UVC(vres_ende_x, vres_ende_y)

        Ekin, x_kin, Ekin_textfeld = self.Ekin_ber(t)
        line_ekin.set_data(x_kin, Ekin)

        x_pot, Epot, Epot_textfeld = self.Epot_ber(t)
        line_epot.set_data(x_pot, Epot)

        h_txt.set_text("h = " + str(np.round(h, decimals=2)) + " m")
        sx_txt.set_text("Strecke = " + str(np.round(sx, decimals=2)) + " m")
        Epot_txt.set_text("Epot = " + str(np.round(Epot_textfeld, decimals=2)) + " Joul")
        Ekin_txt.set_text("Ekin = " + str(np.round(Ekin_textfeld, decimals=2)) + ' Joul')
        vres_txt.set_text("vres = " + str(np.round(v_res, decimals=2)) + " m/s")
        
        return ball, vecy, vecx, vecres, line_ekin, line_epot, h_txt, sx_txt, Epot_txt, Ekin_txt, vres_txt,
```

### Plot erstellen

Es wird vorerst ein Figure erstellt, der 10 Zoll Bereit und 9 Zoll Lang ist. Zusätzlich wird dieses Figure in 18 Zeilen und 20 Spalten eingeteilt.

```python
fig = plt.figure(figsize=(10,9))
gs = fig.add_gridspec(18,20)
```

#### Wurf-Plot

Der Wurf Plot geht von Zeile 6 bis 13 und von Spalte 0 bis 10. 
Für das Objekt wird durch ax.plot() ein Runder Roter Marker in der Größe 15 verwendet.

```python
sxmax, hmax = wurf_instanz1.achsen_ber()

ax = fig.add_subplot(gs[6:13, 0:10])
ax.axis([0,sxmax+0.5,0,hmax+0.5]) # Achsen Skalierung
ax.set_title("Wurf")
ball, = ax.plot([], [], 'ro', ms=15) # Plot für den Ball
```

##### Geschwindigkeitsvektoren

Die Vektoren werden jeweils mit der Funktion ax.quiver() erstellt.

```python
# --------------------- Vektor in y-Richtung erstellen ---------------------

vecy = ax.quiver([0],[wurf_instanz1.h_start],[0],[wurf_instanz1.h_start+wurf_instanz1.vy0], angles='xy', scale_units='xy', scale=4, color='b', label="Vy in m/s")

# --------------------- Vektor in x-Richtung erstellen ---------------------

vecx = ax.quiver([0], [wurf_instanz1.h_start], [0], [wurf_instanz1.vx0], angles='xy', scale_units='xy', scale=4, color='g', label="Vx in m/s")

# --------------------- Resultierender Vektor erstellen ---------------------

vecres = ax.quiver([0], [wurf_instanz1.h_start], [wurf_instanz1.vx0], [wurf_instanz1.vy0], angles='xy', scale_units='xy', scale=4, color='r', label="Vres in m/s")
ax.legend(loc=0)
```

#### Kenetische Energie Plot

Der Plot der Kenetischen Energie geht von Zeile 6 bis 8 und von Spalte 12 bis 20.

```python
Ekin_start, Ekin_min, Ekin_max = wurf_instanz1.Ekin_ber_achsen()

ax = fig.add_subplot(gs[6:8, 12:20])
ax.set_title("Kenetische Energie")
ax.axis([0, wurf_instanz1.tstop[0]+0.5, Ekin_min-1, Ekin_max+0.5])

line_ekin, = ax.plot(0, Ekin_start, 'b', lw=2, label="Kenetische Energie in Joul") # Plot der Kenetischen Energie
ax.grid(True)
```

#### Potenzielle Energie Plot

Der Plot für die Potenzielle Energie geht von der Zeile 11 bis 13 und von der Spalte 12:20.

```python
h_max, Epot_max, Epot_start = wurf_instanz1.Epot_ber_achsen()
ax = fig.add_subplot(gs[11:13, 12:20])
ax.set_title("Potenzielle Energie")
ax.axis([0, wurf_instanz1.tstop[0]+0.03, 0, Epot_max+0.2])

line_epot, = ax.plot(0, Epot_start,'r',lw=2, label="Potenzielle Energie in Joul") # Plot für die Potenzielle Energie
ax.grid(True)
```

#### Plot für die Textfelder

##### Textfelder für die Energien

Die Polts für die Textfelder geht von der Zeile 16 bis 17 und der Spalte 12 bis 20. Die textfelder werden mit der Funktion ax.text() erstellt, der Rahmen wird in box_s definiert.

```python
ax = fig.add_subplot(gs[16:17, 12:20])
box_s = {'facecolor': 'none',
       'edgecolor': 'black',
       'boxstyle': 'square'
      }
ax.set_xticks([])
ax.set_yticks([])
ax.set_frame_on(False)

Ekin_txt = ax.text(0.05, 0.3, '', bbox=box_s) # Textfeld für die Kenetische Energie
Epot_txt = ax.text(0.5, 0.3, '', bbox=box_s) # Textfeld für die Potenzielle Energie
```

##### Textfelder für den Wurf

So Analago auch für die Textfelder für den Wurf, allerdings geht diser Plot von Zeile 16 bis 17 und Spalte 0 : 10.

```python
ax = fig.add_subplot(gs[16:17, 0:10])
ax.set_xticks([])
ax.set_yticks([])
ax.set_frame_on(False)

vres_txt = ax.text(0.05, 0.3, '', bbox=box_s) # Textfeld für die Resultierender Geschwindigkeit
h_txt = ax.text(0.41, 0.3, '', bbox=box_s) # Textfeld für die Höhe
sx_txt = ax.text(0.66, 0.3, '', bbox=box_s) # Textfled für die Strecke
```

#### Animation ausführen

Die Animation ruf die Animate Funktion innerhalb der Klasse Wurf auf.

```python
ani = FuncAnimation(fig, wurf_instanz1.animate_wurf, frames=t, interval=wurf_instanz1.inervall, blit=True) # Animation für den Ball
plt.show()
```

### Hinzufügen der Pause/start Buttons

Die Pause und Start Buttons werden initalisiert, indem man die innerhalb von Matplotlib verfügbaren Widgets verwendet.

```python
ax = fig.add_subplot(gs[0:3, 0:20])
ax.set_xticks([])
ax.set_yticks([])
ax.set_frame_on(False)

ax_box_pause_button = fig.add_axes([0.1, 0.85, 0.10, 0.07])
ax_pause_button = Button(ax_box_pause_button, "Pause")
ax_pause_button.on_clicked(clicked_pause_button)

ax_box_resum_button = fig.add_axes([0.6, 0.85, 0.10, 0.07])
ax_resum_button = Button(ax_box_resum_button, "Resum")
ax_resum_button.on_clicked(clicked_resum_button)
```

Die Funktionen für die Button's werden außerhalb der Klasse Wurf definiert.

```python
def clicked_pause_button(event):
    ani.pause()

def clicked_resum_button(event):
    ani.resume()
```

