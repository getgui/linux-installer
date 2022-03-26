#!../env/bin/python3
primaryColor = "#FBFBFB"
primaryColorLight = "#FFFFFF"
primaryColorDark = "#00838f"
secondaryColor = "#494848"
secondaryColorLight = "#636363"
secondaryColorDark = "#909090"
accentColor = "#00BA34"
accentColorLight = "#17CB49"
accentColorDark = "#00952A"
backgroundColor = "#fafafa"
textColor = "#212121"
textColorLight = "#757575"
textColorDark = "#ffffff"

buttonStyle = f"""
font-size: 15px;
padding: 10px;
margin: 10px;
min-width: 100px;
border: 1px solid {secondaryColorDark};
border-radius: 5px;
"""
titleTextStyle = """
font-size : 20px;
"""
inputTextStyle = """
font-size : 18px;
font-family : "Fira Code", Monaco, monospace;
padding : 10px;
margin : 4px;
"""
installButtonStyle = buttonStyle + f"""
background-color : {accentColorDark};
border-color : {accentColorLight};
color : {primaryColor};
"""