# Im vorliegenden Skript wird ein Schiefer Wurf simuliert und anschließend grafisch animiert.
# Dabei werden sowohl die kinetische als auch die potenzielle Energie berechnet und visualisiert.
# Des Weiteren werden die aktuellen Werte für Geschwindigkeit, kinetische Energie, 
# potenzielle Energie, Höhe und Strecke angezeigt.
# Datum: 12.03.2024
# Version: V1

import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import TextBox, Button

a0 = 45 # Abwurfwinkel in Grad
v0 = 10 # Abwurfgeschwindigkeit in m/s
m = 0.020 # Objektmasse in kg
h_start = 1.5 # Abwurfhöhe in m


class Wurf:
    g = 9.81
    inervall = 6
    n = 300

    def __init__(self, a0_neu, v0_neu, m_neu, h_start_neu):
        self.a0 = np.radians(a0_neu)
        self.v0 = v0_neu
        self.m = m_neu
        self.h_start = h_start_neu
        self.vx0 = np.sin(self.a0) * self.v0
        self.vy0 = np.cos(self.a0) * self.v0

        # Berechnung des Zeitpunktes, bis der Ball auf den Boden kommt
        coeff = [(-1)*(1/2)*self.g, self.vy0, self.h_start]
        h1 = np.poly1d(coeff)
        self.tstop = np.roots(h1)

        # Berechnung des Zeitpunktes, bis der Ball die maximale Höhe erreicht hat
        h1_ab1 = np.polyder(coeff, m=1)
        self.t_hmax = np.roots(h1_ab1)
        

        
    # --------------------- Berechnung der Achsenbeschränkungen des Wurfs ---------------------
    def achsen_ber(self):
        sxmax = self.vx0 * self.tstop[0]
        hmax = self.vy0 * (self.vy0/self.g) - (1/2) * self.g * (self.vy0/self.g)**2 + self.h_start
        return sxmax, hmax
        
    # --------------------- Berechnung der Wurfparabel ---------------------
    def wurf_berechnung(self, t):
        h = self.vy0 * (t) - (1/2) * self.g * (t)**2 + self.h_start
        sx = self.vx0 * (t)
        return h, sx
    
    # --------------------- Berechnung des Vektors in y-Richtung ---------------------
    def vek_ber_y(self, t):
        vy_vektor = self.vy0 - self.g*t

        v_start_y = self.vy0 * (t) - (1/2) * self.g * (t)**2 + self.h_start
        v_start_x = self.vx0 * t

        vy_ende_y = vy_vektor
        vy_ende_x = 0

        return v_start_y, v_start_x, vy_ende_y, vy_ende_x


    # --------------------- Berechnung des Vektors in x-Richtung ---------------------
    def vek_ber_x(self, t):
        v_start_y = self.vy0 * (t) - (1/2) * self.g * (t)**2 + self.h_start
        v_start_x = self.vx0 * t

        v_ende_y = 0
        v_ende_x = self.vx0

        return v_start_y, v_start_x, v_ende_y, v_ende_x
    
    
    # --------------------- Berechnung des Resultierenden Vektors ---------------------
    def vek_ber_res(self, t):
        v_start_y = self.vy0 * (t) - (1/2) * self.g * (t)**2 + self.h_start
        v_start_x = self.vx0 * t

        vres_ende_x = self.vx0
        vres_ende_y = self.vy0 - self.g*t

        v_res = vres_ende_x + vres_ende_y

        return v_start_y, v_start_x, vres_ende_x, vres_ende_y, v_res

    # --------------------- Berechnung der Kenetischen Energie des Balls ---------------------
    def Ekin_ber(self, t):
        x = np.linspace(0, t, int(25*t))
        V_res = np.sqrt((self.vx0)**2 + (self.vy0 - self.g*x)**2)
        Ekin = (1/2) * self.m * (V_res)**2
        Ekin_textfeld = (1/2) * self.m * (np.sqrt((self.vx0)**2 + (self.vy0 - self.g*t)**2))**2
        return Ekin, x, Ekin_textfeld
    
        # --------------------- Berechnung des Starts und Achsen Beschränkungen der Kenetischen Energie ---------------------
    def Ekin_ber_achsen(self):
        Ekin_start = (1/2) * self.m * (self.vx0 + self.vy0)**2
        Ekin_min = (1/2) * self.m * (self.vx0 + (self.vy0 - self.g*self.tstop[0]))**2
        Ekin_max = Ekin_start
        
        return Ekin_start, Ekin_min, Ekin_max

    # --------------------- Berechnung der Potenziellen Energie des Balls ---------------------
    def Epot_ber(self, t):
        x = np.linspace(0, t, int(25*t))
        h = self.vy0 * (x) - (1/2) * self.g * (x)**2 + self.h_start
        Epot = (1/2) * self.m * h**2
        Epot_textfeld = (1/2) * self.m * (self.vy0 * (t) - (1/2) * self.g * (t)**2 + self.h_start)**2

        return x, Epot, Epot_textfeld
    
        # --------------------- Berechnung des Starts und Achsen Beschränkungen der Potenziellen Energie ---------------------
    def Epot_ber_achsen(self):
        h_max = self.vy0 * (self.t_hmax[0]) - (1/2) * self.g * (self.t_hmax[0])**2 + self.h_start
        Epot_max = (1/2) * self.m * (h_max)**2
        Epot_start = (1/2) * self.m * self.h_start

        return h_max, Epot_max, Epot_start

    # --------------------- Animation erstellen ---------------------
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


def clicked_pause_button(event):
    ani.pause()

def clicked_resum_button(event):
    ani.resume()

# -------------------------------------------------------------------------------------------------------------------------------------

wurf_instanz1 = Wurf(a0, v0, m, h_start) # Wurf Klassen-Objekt definieren
t =  np.linspace(0, wurf_instanz1.tstop[0], wurf_instanz1.n) # Zeitdauer des Wurfs definieren



# --------------------- Figure erstellen ---------------------
fig = plt.figure(figsize=(10,9))
gs = fig.add_gridspec(18,20)


# --------------------- Plot für die Wurf-Animation erstellen ---------------------

    # --------------------- Achsenbeschränkungen für den Wurf berechen ---------------------
sxmax, hmax = wurf_instanz1.achsen_ber()

ax = fig.add_subplot(gs[6:13, 0:10])
ax.axis([0,sxmax+0.5,0,hmax+0.5]) # Achsen Skalierung
ax.set_title("Wurf")
ball, = ax.plot([], [], 'ro', ms=15) # Plot für den Ball


# --------------------- Vektor in y-Richtung erstellen ---------------------
vecy = ax.quiver([0],[wurf_instanz1.h_start],[0],[wurf_instanz1.h_start+wurf_instanz1.vy0], angles='xy', scale_units='xy', scale=4, color='b', label="Vy in m/s")


# --------------------- Vektor in x-Richtung erstellen ---------------------
vecx = ax.quiver([0], [wurf_instanz1.h_start], [0], [wurf_instanz1.vx0], angles='xy', scale_units='xy', scale=4, color='g', label="Vx in m/s")

# --------------------- Resultierender Vektor erstellen ---------------------
vecres = ax.quiver([0], [wurf_instanz1.h_start], [wurf_instanz1.vx0], [wurf_instanz1.vy0], angles='xy', scale_units='xy', scale=4, color='r', label="Vres in m/s")

ax.legend(loc=0)
# --------------------- Plot für die Kenetische Energie erstellen ---------------------

    # --------------------- Achsen begrenzungen für die Kenetische Energie bestimmen ---------------------
Ekin_start, Ekin_min, Ekin_max = wurf_instanz1.Ekin_ber_achsen()

ax = fig.add_subplot(gs[6:8, 12:20])
ax.set_title("Kenetische Energie")
ax.axis([0, wurf_instanz1.tstop[0]+0.5, Ekin_min-1, Ekin_max+0.5])
line_ekin, = ax.plot(0, Ekin_start, 'b', lw=2, label="Kenetische Energie in Joul") # Plot der Kenetischen Energie
ax.grid(True)

# --------------------- Plot für die Potenzielle Energie erstellen ---------------------

    # --------------------- Achsen begrenzungen für die Potenzielle Energie bestimmen ---------------------
h_max, Epot_max, Epot_start = wurf_instanz1.Epot_ber_achsen()

ax = fig.add_subplot(gs[11:13, 12:20])
ax.set_title("Potenzielle Energie")
ax.axis([0, wurf_instanz1.tstop[0]+0.03, 0, Epot_max+0.2])
line_epot, = ax.plot(0, Epot_start,'r',lw=2, label="Potenzielle Energie in Joul") # Plot für die Potenzielle Energie
ax.grid(True)


# --------------------- Plot für die Textfelder ---------------------
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


ax = fig.add_subplot(gs[16:17, 0:10])
ax.set_xticks([])
ax.set_yticks([])
ax.set_frame_on(False)
vres_txt = ax.text(0.05, 0.3, '', bbox=box_s) # Textfeld für die Resultierender Geschwindigkeit
h_txt = ax.text(0.41, 0.3, '', bbox=box_s) # Textfeld für die Höhe
sx_txt = ax.text(0.66, 0.3, '', bbox=box_s) # Textfled für die Strecke


# --------------------- Plot für Button's ---------------------
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


# --------------------- Animation ---------------------
ani = FuncAnimation(fig, wurf_instanz1.animate_wurf, frames=t, interval=wurf_instanz1.inervall, blit=True) # Animation für den Ball

plt.show()