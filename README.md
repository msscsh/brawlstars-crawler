# bs-club-mngr
A project to manage clubs in Brawl Stars


## Config file and host

Create a .env file with content(Use your own values for the following keys)

touch ./.env
```
    SPREADSHEETID=xcksjcikn381293jdnks
    PLAYERSTAB=Sheet1
    PLAYERSCELLS=A2:Z
```

Create the following environment variables on the host(Use your own values)

```
    CLUBTAG=999999999
    BS_EMAIL=email@email.com
    BS_PASSWORD=theStrongestPassword
    EXTERNAL_IP=YOU_EXTERNAL_IP
```

Add your favicon in the following path

./src/commons/files/

Add your google spreadsheet credential json in this locantion, with this name:
./src/commons/files/credentials.json

## Club config

Create the list of times the server menu
http://localhost:1337/teams

Send data to the spreadsheet
http://localhost:1337/



## Dev's Remembrall

Report from ESLint + Prettier

```
    #Get a report
    npx eslint .

    #Auto fix issues
    npx eslint . --fix
```

Project stages

```
    #Separated
    npm run codereview
    npm run keys
    npm run files
    npm run build
    npm run server

    #One stage to rule then all (no code review)
    npm run pipeline
```
