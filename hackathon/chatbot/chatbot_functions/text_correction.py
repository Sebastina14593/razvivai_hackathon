def number_correction(text):
    text = (text.replace("1. ", "<br>1. ")
                .replace(" 2. ", "<br>2. ")
                .replace(" 3. ", "<br>3. ")
                .replace(" 4. ", "<br>4. ")
                .replace(" 5. ", "<br>5. ")
                .replace(" 6. ", "<br>6. ")
                .replace(" 7. ", "<br>7. ")
                .replace(" 8. ", "<br>8. ")
                .replace(" 9. ", "<br>9. ")
            )
    return text