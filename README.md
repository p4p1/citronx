# citronx
A tool to enumerate citrix web applications through the webapp store.

## usage
``` bash
citronx: A slick citrix scanner made by p4p1
        -h      --help - Show this message.
        -g      --gui - A gui interface to view your citrix apps and run them.
        -s      --scan - Get all of the configuration from citrix and application data from each user.
        -c      --conf - Provide a different config file.
```

### Examples
``` bash
citronx -c ./config.json --gui
```

## Config file example
to run ica files you need to donwload the citrix client side application [here](https://www.citrix.com/downloads/workspace-app/linux/workspace-app-for-linux-latest.html)
``` json
{
    "server": "localhost/citrix/WebStore/",
    "run_ica": "/home/p4p1/Documents/work/mm/vie/wk_inst/linuxx64/wfica.sh",
    "secure": false,
    "users": [
        {
            "username": "domain\\user",
            "password": "password"
        }
    ]
}
```

## GUI screenshot
![image](https://github.com/user-attachments/assets/923c1362-9735-4213-a48c-6a6834ef27c5)
