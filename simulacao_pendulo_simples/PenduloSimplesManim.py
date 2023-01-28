from manim import *

class Pendulo(Scene):
    def construct(self):
        time = ValueTracker(0)
        theta_max = 30/100 * PI
        L = 3
        g = 9.8
        w = np.sqrt(g/L)
        T = 2*PI/w
        p_x = -2.5
        p_y = 3
        shift_req = p_x*RIGHT + p_y*UP

        theta = DecimalNumber().set_color(BLACK).move_to(10*RIGHT)
        theta.add_updater(lambda m: m.set_value((theta_max)*np.sin(w*time.get_value())))

        self.add(theta)

        # Cria a linha:
        def get_line(x,y):
            line_here = Line(start = ORIGIN + shift_req, end = x*RIGHT + y*UP + shift_req, color=GREY)
            global line_vertical
            line_vertical = DashedLine(start = line_here.get_start(), end = line_here.get_start() + 3*DOWN, color=GREY)

            return line_here

        line = always_redraw(lambda : get_line(L*np.sin(theta.get_value(),-L*np.cos(theta.get_value()))))

        self.add(line)
        self.add(line_vertical)

        # Cria arco do angulo:
        def angle_arc(theta):
            global angle
            global arch_text
            if theta == 0:
                angle = VectorizedPoint().move_to(10*RIGHT)
                arch_text = VectorizedPoint().move_to(10*RIGHT)
            else:
                if (theta>0):
                    angle = Angle(line,line_vertical, quadrant=(1,1), other_quadrant=True, color=YELLOW, fill_opacity=0)
                
                elif (theta<0):
                    angle = Angle(line,line_vertical, quadrant=(1,1), other_quadrant=False, color=YELLOW, fill_opacity=0)

            return angle

        angle = always_redraw(lambda: angle_arc(theta.get_value()))
        set.add(angle)
        arch_text = Tex(r'$\theta$').scale(0.5)
        arch_text.add_updater(lambda m: m.next_to(angle,DOWN))
        self.add(arch_text)

        self.play(time.animate.set_value(3*T),rate_func=linear, run_time=3*T)



