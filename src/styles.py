#!../env/bin/python3
primaryColor = "#FBFBFB"
primaryColorLight = "#FFFFFF"
primaryColorDark = "#dbdbdb"
secondaryColor = "#636363"
secondaryColorLight = "#adadad"
secondaryColorDark = "#494848"
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
border: 1px solid {secondaryColorLight};
border-radius: 5px;
"""
titleTextStyle = """
font-size : 20px;
margin: 10px 0 0 0;
"""

normalTextStyle = f"""
font-size: 18px;
padding: 10px 0 0 0;
color: {primaryColorDark};
"""
subtextStyle = normalTextStyle + f"""
font-size: 14px;
color: {secondaryColorLight};
"""
mediumTextStyle = normalTextStyle + f"""
font-size: 16px;
color: {textColorLight};
margin: 0 10px 0 0;
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