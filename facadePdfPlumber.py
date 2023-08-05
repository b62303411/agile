

class FacadePdfPlumber:
    def search_dataframe(df, search_term):
        return df[df.apply(lambda row: row.astype(str).str.contains(search_term).any(), axis=1)]
    def crop(page, box):
        print("crop:" + str(box))
        cropped_page = page.crop((box.left, box.top, box.right_crop, box.bottom_crop))
        print("cropped: width" + str(cropped_page.width) + " Height:" + str(cropped_page.height))
        return cropped_page
    def convertToImage(cropped_page):
        #time.sleep(1)
        print("convert to image")
        print("cropped: width" + str(cropped_page.width) + " Height:" + str(cropped_page.height))
        cropped_image = cropped_page.to_image(resolution=300)
        print("image done")
        #time.sleep(1)
        return cropped_image