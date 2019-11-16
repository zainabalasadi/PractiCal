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
        }
        this.handleNlpCreation = this.handleNlpCreation.bind(this);
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
                onClick={() => {
                      this.getCalList();
                    }}>
                CLICK ME
                </Button>
{/*                 TODO NEED TO FIX THIS UP*/}
                <div>{this.state.calendars}</div>
            </Drawer>
        );
    }
}

export default withStyles(styles)(Sidebar);