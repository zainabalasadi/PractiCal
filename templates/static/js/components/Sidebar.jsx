import React, { Component } from "react";
import { Drawer } from "@material-ui/core";
import { withStyles } from "@material-ui/core/styles";
import Input from '@material-ui/core/Input';
import { Dialog, DialogTitle, DialogContent, Button, TextField, Typography } from "@material-ui/core";
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemSecondaryAction from '@material-ui/core/ListItemSecondaryAction';
import ListItemText from '@material-ui/core/ListItemText';
import Checkbox from '@material-ui/core/Checkbox';
import IconButton from '@material-ui/core/IconButton';
import MoreVertIcon from '@material-ui/icons/MoreVert';
import AddIcon from '@material-ui/icons/Add';
import CloseIcon from '@material-ui/icons/Close';
import { CirclePicker } from 'react-color'

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
        root: {
        width: '100%',
        maxWidth: 360,
        backgroundColor: theme.palette.background.paper,
        paddingLeft: 0,
    },
    check: {
        minWidth: 10,
    },
    addButton: {
        position: 'absolute',
        right: theme.spacing(5),
        top: theme.spacing(17),
    },
    closeButton: {
        position: 'absolute',
        right: theme.spacing(1),
        top: theme.spacing(1),
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
            checked: 0,
            setChecked: 0,
            createPopUp: false,
            calName: "",
            calColour: "",
        }
        this.handleNlpCreation = this.handleNlpCreation.bind(this);
        this.handleCreateOpen = this.handleCreateOpen.bind(this);
        this.handleClose = this.handleClose.bind(this);
        this.renderNotifList = this.renderNotifList.bind(this)
    }
        componentDidMount() {
        console.log('calling...')
        this.getCalList()
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

    create_calendar(calendar) {
        let response = fetch('/createCalendar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8'
            },
        body: JSON.stringify({"name": calendar.name, "colour": calendar.colour})
        }).then((data) => data.json()).then(cal => {
            console.log(cal.success);
            if (cal.success) {
                console.log("Created calendar successfully")
                console.log(calendar)
                this.state.calendars.push(calendar)
            } else {
                console.log("Failed calendar creation")
            }
        });
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
                new_list.push(calList.calendars[i])
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
            <h10>
                {e.title}
                <br></br>
                {e.sender}
                <br></br>
                {e.start}
                <br></br>
                {e.type}
            </h10>
        )
   }

    handleCreateOpen() {
        this.setState ({ createPopUp: true });
    };

    handleClose() {
        this.setState({ createPopUp: false });
    }

    setCalName = e => { 
        this.setState({ name: e }); 
    };

    setCalColour = e => { 
        this.setState({ colour: e.hex }); 
    };

    setNewCalendar() {
        const { name, colour } = this.state;
        let newCal = { name, colour };
        let calendars = this.state.calendars.slice();
        calendars.push(newCal);
        this.setState({ calendars });
        this.create_calendar(newCal)
    }

    handleToggle = value => () => {
        // const currentIndex = this.state.checked.indexOf(value);
        // const newChecked = [...this.state.checked];
        // if (currentIndex === -1) {
        //   newChecked.push(value);
        // } else {
        //   newChecked.splice(currentIndex, 1);
        // }

        // this.state.setChecked(newChecked);
    };


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
                <div>
                    <h3>My Calendars</h3>
                    <IconButton className={classes.addButton} edge="end" onClick={this.handleCreateOpen}>
                        <AddIcon />
                    </IconButton>
                </div>
                <List>
                {this.state.calendars.map(item => {
                    const labelId = `checkbox-list-label-${item.name}`;
                    return (
                    <ListItem className={classes.root} key={item.name} role={undefined} dense button onClick={this.handleToggle(item)}>
                        <ListItemIcon className={classes.check}>
                            <Checkbox
                            className={classes.check}
                            edge="start"
                            //checked={this.state.checked.indexOf(item) !== -1}
                            tabIndex={-1}
                            disableRipple
                            inputProps={{ 'aria-labelledby': labelId }}
                            />
                        </ListItemIcon>
                        <ListItemText id={labelId} primary={`${item.name}`} />
                            <ListItemSecondaryAction>
                                <IconButton edge="end" /*onClick={this.handleMenuOpen}*/>
                                    <MoreVertIcon />
                                </IconButton>
                            </ListItemSecondaryAction>
                        </ListItem>
                    );
                    })}
                    </List>
                <h3>My Notifs</h3>
                <Button
                label="notifs"
                onClick={() => {
                      this.getNotifList();
                    }}>
                NO CLICK ME
                </Button>
                {this.renderObject()}
                
                {/* Modal to create new calendar */}
                <Dialog open={this.state.createPopUp} onClose={this.handleClose}>
                    <IconButton aria-label="close" className={classes.closeButton} onClick={this.handleClose}>
                        <CloseIcon />
                    </IconButton>
                    <DialogTitle id="customized-dialog-title" onClose={this.handleClose}>
                        Create a new calendar
                    </DialogTitle>
                    <DialogContent>
                        <TextField 
                          placeholder="Calendar Name"
                          margin="dense"
                          onChange={e => {
                            this.setCalName(e.target.value);
                          }}
                        />
                        <CirclePicker 
                          color={ this.state.colour }
                          onChangeComplete={ this.setCalColour }
                        />
                        <Button
                          label="Create Contact"
                          variant="contained" 
                          color="primary"
                          onClick={() => {
                            this.setNewCalendar(), this.handleClose();
                          }}
                        >
                        Create Calendar
                        </Button>
                    </DialogContent>
                </Dialog>
            </Drawer>
        );
    }
}

export default withStyles(styles)(Sidebar);