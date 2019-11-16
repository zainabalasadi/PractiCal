import React, { Component } from "react";
import { Drawer } from "@material-ui/core";
import { withStyles } from "@material-ui/core/styles";
import Input from '@material-ui/core/Input';
import { Dialog, DialogTitle, DialogContent, Button, TextField, Typography } from "@material-ui/core";

const drawerWidth = 300;
const navHeight = 64;

const styles = theme => ({
    drawer: {
        marginTop: navHeight,
        width: drawerWidth,
        flexShrink: 0,
    },
    drawerPaper: {
        marginTop: navHeight,
        width: drawerWidth,
        padding: theme.spacing(3),
    },
    input: {
        marginBottom: theme.spacing(8),
    },
});



class Sidebar extends Component {  
    constructor() {
        super()
        this.state = {
            nlpText: "",
            calendars: [
            ],
            notifs: [
            ],
        }
        this.handleNlpCreation = this.handleNlpCreation.bind(this);
        this.renderNotifList = this.renderNotifList.bind(this)
    }

    handleNlpCreation(e) {
        console.log(e.target.value)
        const response = fetch('/getIntent', {
          method: 'POST',
          body: JSON.stringify({"nlpText": e.target.value}),
          headers: {
            'Content-Type': 'application/json;charset=utf-8'
          }
        }).then(response => response.json()).then(data => console.log(data))
        // TODO Insert code to reflect changes in back end on the front end given the 
        // response from the fetch request
    }

    getCalList() {
        let response = fetch('/getEvents', {
            method: 'GET'

        }).then((data) => data.json()).then(data => this.renderCalList(data));
    }

    renderCalList(calList) {
        console.log(calList)
        var new_list = new Array()
        console.log(calList.calendars)
        for (var i = 0 ; i < calList.calendars.length ; i++) {
                console.log(calList.calendars[i].name)
                new_list.push(calList.calendars[i].name)
        }

        this.setState((prevState) => {
            calendars: Array.prototype.push.apply(prevState.calendars, new_list)
        })

        this.render()
        this.forceUpdate()
    }



   getNotifList() {
        let response = fetch('/getNotifs', {
            method: 'GET'

        }).then((data) => data.json()).then(data => this.renderNotifList(data));
    }

    renderNotifList(calList) {
        console.log(calList)
        var new_list1 = new Array()
        for (var i = 0 ; i < calList.length ; i++) {
                console.log(calList[i])
                new_list1.push(calList[i])
        }

        this.setState((prevState) => {
            notifs: Array.prototype.push.apply(prevState.notifs, new_list1)
        })

        this.render()
        this.forceUpdate()
    }


   renderObject(){
    for (var i = 0 ; i < this.state.notifs.length ; i++) {
       return (
           this.renderNotifListsss(this.state.notifs[i])
       )
    }
   }

   renderNotifListsss(e) {
        console.log(e.title)
        return (
            <h5>
                {e.title}
                <br></br>
                {e.sender}
                <br></br>
                {e.start}
                <br></br>
                {e.end}
            </h5>
        )
   }


    render() {
        const { classes } = this.props;
        return (
            <Drawer
              className={classes.drawer}
              variant="permanent"
              anchor="right"
              classes={{
                paper: classes.drawerPaper,
              }}
            >
                <h3>Add a Quick Event</h3>
                <Input
                  className={classes.input}
                  placeholder="Lunch at 2 tomorrow"
                  inputProps={{
                    'aria-label': 'description',
                  }}
                  value={ this.state.nlpText }
                  onChange={e => {
                    this.setState({ nlpText: e.target.value})
                  }}
                  onKeyPress={ e => {
                    if (e.key === "Enter") {
                      this.handleNlpCreation(e)
                    }
                  }}
                />
                <h3>My Calendars</h3>
                <Button
                label="cal"
                onClick={() => {
                      this.getCalList();
                    }}>
                CLICK ME
                </Button>
{/*                 TODO NEED TO FIX THIS UP*/}
                <div>{this.state.calendars}</div>
                <h3>My Notifs</h3>
                <Button
                label="notifs"
                onClick={() => {
                      this.getNotifList();
                    }}>
                NO CLICK ME
                </Button>
                {this.renderObject()}
            </Drawer>
        );
    }
}

export default withStyles(styles)(Sidebar);