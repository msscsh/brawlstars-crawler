# bs-club-mngr
A project to manage clubs in Brawl Stars


## Always remember
```
    npm run build
```

## Star server
```
    npm run server
```

## Config file and host

Create a .env file with content(Use your own values for the following keys)

./.env
```
    SPREADSHEETID=xcksjcikn381293jdnks
    SPREADSHEETTAB=Sheet1
    PLAYERCELLS=A:Z
```

Create the following environment variables on the host(Use your own values)

```
    export CLUBTAG=999999999
    export BS_EMAIL=email@email.com
    export BS_PASSWORD=theStrongestPassword
    expost EXTERNAL_IP=YOU_EXTERNAL_IP
```

## Club config

Create a team list file with the following format(one line per team for each team)

./src/commons/files/team_relation.txt
```
    TEAM_A:TAG_PLAYER_A_1;TAG_PLAYER_A_2;TAG_PLAYER_A_3;
```

