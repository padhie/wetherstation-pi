from waveshare_epd import epd7in5_V2

def display_on_eink(epd7in5_V2, img):
    epd = epd7in5_V2.EPD()
    epd.init()
    epd.display(epd.getbuffer(img))
    epd.sleep()