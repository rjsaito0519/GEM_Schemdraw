from typing import Optional, Sequence
import schemdraw
import schemdraw.elements as elm
import matplotlib.pyplot as plt
from schemdraw.segments import Segment, SegmentPoly, SegmentText
import numpy as np


# Drawingオブジェクトの作成とサイズの設定
d = schemdraw.Drawing()
d.config(fontsize=18, unit=2, inches_per_unit=1, font='Times New Roman')  # フォントサイズと単位サイズを指定

class GEM(elm.Element):
    _element_defaults = {
        'switchcolor': '#333333',
    }
    def __init__(self, *,
                 gem_width: float = 10,
                 n_section: int = 6,
                 pattern: Optional[Sequence[bool]] = None,
                 switchcolor: Optional[str] = None,
                 **kwargs):
        super().__init__(**kwargs)


        # +-----+
        # | GEM |
        # +-----+
        sec_width = gem_width/n_section
        margin = gem_width * 0.02

        body = [
            [0, 0],
            [gem_width, 0],
            [gem_width, gem_width*np.tan(np.pi/8)],
            [gem_width*np.tan(np.pi/8), gem_width],
            [0, gem_width]
        ]
        self.segments.append(SegmentPoly(
            body,
            fill="#efbc3f",
            lw = 1
        ))

        border = [
            [-margin, -margin],
            [gem_width+margin, -margin],
            [gem_width+margin, gem_width*np.tan(np.pi/8)+(np.sqrt(2)-1)*margin],
            [gem_width*np.tan(np.pi/8)+(np.sqrt(2)-1)*margin, gem_width+margin],
            [-margin, gem_width+margin]
        ]
        self.segments.append(SegmentPoly(
            border,
            lw = 1
        ))
        
        gnd = [
            [gem_width-sec_width/3, -margin],
            [gem_width+margin, -margin],
            [gem_width+margin, sec_width/5],
            [gem_width-sec_width/3, sec_width/5]
        ]
        self.segments.append(SegmentPoly(
            gnd,
            fill="#525659"
        ))

        def y(x):
            if x < gem_width*np.tan(np.pi/8):
                return gem_width
            else:
                return -x + gem_width*(1+np.tan(np.pi/8))

        for i in range(n_section):
            sec_body = []
            sec_body.append([sec_width*i, 0])
            sec_body.append([sec_width*(i+1), 0])
            sec_body.append([sec_width*(i+1), y(sec_width*(i+1))])
            if sec_width*i < gem_width*np.tan(np.pi/8) and gem_width*np.tan(np.pi/8) < sec_width*(i+1):
                sec_body.append([gem_width*np.tan(np.pi/8), gem_width])
            sec_body.append([sec_width*i, y(sec_width*i)])
            self.segments.append(SegmentPoly(
                sec_body,
                lw = 0.5,
                ls = "--"
            ))
        # self.segments.append(SegmentText((sec_width/2, y(sec_width*(n_section-1)+sec_width/2)/2), 'seg. 1', fontsize=18, rotation=90))
        # self.segments.append(SegmentText((sec_width*(n_section-1)+sec_width/2, y(sec_width*(n_section-1)+sec_width/2)/2), 'seg. {}'.format(n_section), fontsize=18, rotation=90))
        
        # +------------+
        # | dip switch |
        # +------------+
        spacing = gem_width*2/3 / (3*n_section+5)
        dip_width  = spacing*2
        switch_height = 6*spacing
        switch_width  = gem_width * 2/3
        diff_g2s = gem_width - switch_width
        dis = gem_width/7

        switch_border = [
            [diff_g2s/2, -dis-switch_height],
            [diff_g2s/2+gem_width*2/3, -dis-switch_height],
            [diff_g2s/2+gem_width*2/3, -dis],
            [diff_g2s/2, -dis]
        ]
        self.segments.append(SegmentPoly(
            switch_border,
            lw = 1
        ))
        for i in range(n_section):
            ref_x = diff_g2s/2 + dip_width*i + spacing*(i+1)
            ref_y = -dis - spacing
            on = pattern and pattern[i]
            off = pattern and not pattern[i]
            self.segments.append(SegmentPoly(
                ([ref_x, ref_y], [ref_x+dip_width, ref_y], [ref_x+dip_width, ref_y-dip_width], [ref_x, ref_y-dip_width]),
                fill=self.params['switchcolor'] if on else None,
                lw = 1
            ))  # On
            self.segments.append(SegmentPoly(
                ([ref_x, ref_y-dip_width], [ref_x+dip_width, ref_y-dip_width], [ref_x+dip_width, ref_y-2*dip_width], [ref_x, ref_y-2*dip_width]),
                fill=self.params['switchcolor'] if off else None,
                lw = 1
            ))  # Off
            self.anchors[f'ch{i+1}'] = (ref_x+dip_width/2, ref_y-2*dip_width)

        ref_x = diff_g2s/2 + dip_width*n_section + spacing*(n_section+2)
        ref_y = -dis - spacing
        self.segments.append(SegmentPoly(
            ([ref_x, ref_y], [ref_x+dip_width, ref_y], [ref_x+dip_width, ref_y-dip_width], [ref_x, ref_y-dip_width]),
            fill=self.params['switchcolor'],
            lw = 1
        ))  # On
        self.segments.append(SegmentPoly(
            ([ref_x, ref_y-dip_width], [ref_x+dip_width, ref_y-dip_width], [ref_x+dip_width, ref_y-2*dip_width], [ref_x, ref_y-2*dip_width]),
            lw = 1
        ))  # Off
        self.anchors['gnd'] = (ref_x+dip_width/2, ref_y-2*dip_width)
            

        # self.segments.append(SegmentText(
        #     (diff_g2s/2-spacing, -dis - dip_width/2),
        #     'on', fontsize=16, align=["right", "bottom"]
        # ))
        # self.segments.append(SegmentText(
        #     (diff_g2s/2-spacing, -dis - 2*spacing - dip_width*3/2),
        #     'off', fontsize=16, align=["right", "top"]
        # ))

        # +------+
        # | line |
        # +------+
        vline_height = dis/5
        for i in range(n_section):   
            ref_x = diff_g2s/2 + dip_width*i + spacing*(i+1)
            ref_y = -dis - spacing
            self.segments.append(Segment(
                [ (sec_width/2 + sec_width*i, 0), (sec_width/2 + sec_width*i, -vline_height), (ref_x+dip_width/2, ref_y+vline_height), (ref_x+dip_width/2, ref_y) ],
                lw = 1.1
            ))
        # gnd
        ref_x = diff_g2s/2 + dip_width*n_section + spacing*(n_section+2)
        ref_y = -dis - spacing
        self.segments.append(Segment(
            [ (gem_width, -margin), (gem_width, -vline_height), (ref_x+dip_width/2, ref_y+vline_height), (ref_x+dip_width/2, ref_y) ],
            lw = 1.1
        ))


        # +----------+
        # | resistor |
        # +----------+
        res_width  = sec_width*3/5
        res_height = res_width*5/2
        def resistor(start_x, start_y, is_vertical = False):
            if is_vertical:
                return [
                    (start_x-res_width/2, start_y),
                    (start_x+res_width/2, start_y),
                    (start_x+res_width/2, start_y-res_height),
                    (start_x-res_width/2, start_y-res_height)
                ]
            else:
                return [
                    (start_x, start_y-res_width/2),
                    (start_x, start_y+res_width/2),
                    (start_x+res_height, start_y+res_width/2),
                    (start_x+res_height, start_y-res_width/2)
                ]
            

        for i in range(n_section):   
            ref_x = diff_g2s/2 + dip_width*i + spacing*(i+1)
            ref_y = -dis - spacing
            self.segments.append(Segment(
                [ (ref_x+dip_width/2, ref_y-2*dip_width), (ref_x+dip_width/2, ref_y-2*dip_width-vline_height),
                  (sec_width/2 + sec_width*i, ref_y-2*dip_width-spacing-dis+vline_height), (sec_width/2 + sec_width*i, ref_y-2*dip_width-spacing-dis) ],
                lw = 1.1
            ))
            self.segments.append(SegmentPoly(resistor(sec_width/2 + sec_width*i, ref_y-2*dip_width-spacing-dis, is_vertical=True), lw = 1))
        # gnd
        ref_x = diff_g2s/2 + dip_width*n_section + spacing*(n_section+2)
        ref_y = -dis - spacing
        self.segments.append(Segment(
            [ (ref_x+dip_width/2, ref_y-2*dip_width), (ref_x+dip_width/2, ref_y-2*dip_width-vline_height),
              (sec_width/2 + sec_width*n_section, ref_y-2*dip_width-spacing-dis+vline_height), (sec_width/2 + sec_width*n_section, ref_y-2*dip_width-spacing-dis) ],
            lw = 1.1
        ))
        self.segments.append(SegmentPoly(resistor(sec_width/2 + sec_width*n_section, ref_y-2*dip_width-spacing-dis, is_vertical=True), lw = 1))


        # +---------------+
        # | to main chain |
        # +---------------+
        for i in range(n_section):   
            self.segments.append(Segment(
                [ (sec_width/2 + sec_width*i, ref_y-2*dip_width-spacing-dis-res_height), (sec_width/2 + sec_width*i, ref_y-2*dip_width-spacing-dis-res_height-2*vline_height) ],
                lw = 1.1
            ))
        self.segments.append(Segment(
            [ 
                (sec_width/2 + sec_width*(n_section-1), ref_y-2*dip_width-spacing-dis-res_height-2*vline_height),
                (sec_width/2, ref_y-2*dip_width-spacing-dis-res_height-2*vline_height),
                (sec_width/2, ref_y-2*dip_width-spacing-dis-res_height-2*dis)
            ],
            lw = 1.1
        ))
        # gnd
        self.segments.append(Segment(
            [ 
                (sec_width/2 + sec_width*n_section, ref_y-2*dip_width-spacing-dis-res_height),
                (sec_width/2 + sec_width*n_section, ref_y-2*dip_width-spacing-dis-res_height-dis),
                ((gem_width+sec_width)/2, ref_y-2*dip_width-spacing-dis-res_height-dis),
                ((gem_width+sec_width)/2, ref_y-2*dip_width-spacing-dis-res_height-2*dis),
            ],
            lw = 1.1
        ))

        diff_g2r = gem_width/2 - res_height
        self.segments.append(SegmentPoly(resistor(diff_g2r/2+sec_width/2, ref_y-2*dip_width-spacing-dis-res_height-2*dis, is_vertical=False), lw = 1))
        self.segments.append(SegmentPoly(resistor(diff_g2r/2+(gem_width+sec_width)/2, ref_y-2*dip_width-spacing-dis-res_height-2*dis, is_vertical=False), lw = 1))
        
        self.segments.append(Segment(
            [ 
                (diff_g2r/2+sec_width/2, ref_y-2*dip_width-spacing-dis-res_height-2*dis),
                (-gem_width/7, ref_y-2*dip_width-spacing-dis-res_height-2*dis)
            ],
            lw = 1.1
        ))
        self.segments.append(Segment(
            [ 
                (diff_g2r/2+sec_width/2+res_height, ref_y-2*dip_width-spacing-dis-res_height-2*dis),
                (diff_g2r/2+(gem_width+sec_width)/2, ref_y-2*dip_width-spacing-dis-res_height-2*dis)
            ],
            lw = 1.1
        ))
        self.segments.append(Segment(
            [ 
                (diff_g2r/2+(gem_width+sec_width)/2+res_height, ref_y-2*dip_width-spacing-dis-res_height-2*dis),
                (gem_width+gem_width/7, ref_y-2*dip_width-spacing-dis-res_height-2*dis)
            ],
            lw = 1.1
        ))
        

gem = d.add(GEM(gem_width=5, n_section=6, pattern=[False, False, False, True, False, False]))


d.save('circuit_custom_size.png', dpi=300)
d.draw()