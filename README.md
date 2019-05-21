# Frevo

*Hosted at [GitHub](https://github.com/matuzalemmuller/frevo) and mirrored to [GitLab](https://gitlab.com/matuzalemmuller/frevo).*

## Description

Run customizable commands in terminal directly from the Mac top bar!

![](https://i.imgur.com/ymocru0.png)

![](https://i.imgur.com/S787zXy.png)

![](https://media.giphy.com/media/5wFIpb7YYnHnpNuDic/giphy.gif)

## Installation

You can download the `.dmg` package [here](https://github.com/matuzalemmuller/Frevo/releases).

After dowloading the package, simply click in the `.dmg` file to mount it in your Mac and move the file `Frevo.app` to the "Applications" folder.

To start Frevo when the system starts, go to "System Preferences" -> "Users & Groups" -> "Login Items" and add Frevo to the list.

## Contributing

Feel free to fork and/or star the project. 

----

## Next steps

The unpacked app has around 65 MB, which is not a lot considering the super computers that we have nowadays. However, some system tray apps have less than 10 MB. The reason why Frevo takes more space is because I had to embed the PyQt libraries used by the app so it could run in multiple versions of OSX without having to manually install a specific version of Python and/or PyQt. Just the PyQt libraries take around 60 MB of space, which justifies the size of the app.

The next step for this project is converting it to a full Swift/Objective C app for Mac and porting it to Linux and other platforms.
