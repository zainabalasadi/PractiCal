import React, { Component } from "react";
import { Calendar, momentLocalizer} from 'react-big-calendar';
import { Dialog, DialogActions, DialogContent, Button, TextField } from "@material-ui/core";
import { InputLabel, Select, CssBaseline } from '@material-ui/core/';
// import { InputLabel, Select, CssBaseline } from '@material-ui/core/';
import moment from "moment";
import Navbar from './Navbar'
import Sidebar from './Sidebar'

import "!style-loader!css-loader!react-big-calendar/lib/css/react-big-calendar.css";
import { withStyles } from "@material-ui/core/styles";


// Initialise time localiser
const localizer = momentLocalizer(moment)

const drawerWidth = 300;
const navHeight = 64;

const styles = theme => ({
    calendar: {
        height: `calc(100% - ${navHeight}px - 43px)`, 
        position: "fixed", 
        width: `calc(100% - ${drawerWidth}px + 1px)`,
        marginLeft: "15px"
    },
    root: {
        display: 'flex',
    },
    appBar: {
        zIndex: theme.zIndex.drawer + 1,
    },
    drawer: {
        width: drawerWidth,
        flexShrink: 0,
    },
    drawerPaper: {
        width: drawerWidth,
        padding: theme.spacing(3),
    },
    content: {
        flexGrow: 1,
    },
    toolbar: theme.mixins.toolbar,
    title: {
        fontSize: 100,
        margin: '20px 0 20px 0',
    },
    inputMargin: {
        margin: '8px 0 8px 0',
    },
});


// Load events
class Cal extends Component {  
    constructor() {
        super();
        this.state = {
            // Loading sample events, remove later
            events: [  

            ],
            title: "",
            start: "",
            end: "",
            desc: "",
            invitees: "",
            groups: "",
            calendar: "",
            eventId: "",
            openSlot: false,
            openEvent: false,
            clickedEvent: {},
        };
        this.handleClose = this.handleClose.bind(this);
    };

    // Function to create event and send to back-end
    create_event(event) {
        console.log(event)
        // console.log(event.state)
        console.log(JSON.stringify({"name": event.title, "desc": event.desc, 
                                    "startDate": event.start, "endDate": event.end, "invitees": event.invitees,
                                    "groups": event.groups, "calendar": event.calendar, "eventId": event.eventId}))
        let response = fetch('/createEvent', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8'
            },
        body: JSON.stringify({"name": event.title, "desc": event.desc, 
                            "startDate": event.start, "endDate": event.end, "invitees": event.invitees,
                            "groups": event.groups, "calendar": event.calendar, "eventId": event.eventId})
        }).then((data) => data.json()).then(event => {
            console.log(event.success);
            if (event.success) {
                // append to events list
                console.log("Created event successfully")
                this.state.events.push(event)
            } else {
                console.log("Failed event creation")
            }
        });
    }

    // Function to edit event in back-end
    edit_event(event) {
        console.log(JSON.stringify({"name": event.title, "desc": event.desc, 
                                    "startDate": event.start, "endDate": event.end, "invitees": event.invitees,
                                    "groups": event.groups, "calendar": event.calendar, "eventId": event.eventId}))
        let response = fetch('/editEvent', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8'
            },
        body: JSON.stringify({"name": event.title, "desc": event.desc, 
                            "startDate": event.start, "endDate": event.end, "invitees": event.invitees,
                            "groups": event.groups, "calendar": event.calendar, "eventId": event.eventId})
        }).then((data) => data.json());
    }

    delete_event(event) {
        console.log(JSON.stringify({"name": event.title, "desc": event.desc,
                                    "startDate": event.start, "endDate": event.end, "invitees": event.invitees,
                                    "groups": event.groups, "calendar": event.calendar, "eventId": event.eventId}))
        let response = fetch('/deleteEvent', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8'
            },
        body: JSON.stringify({"name": event.title, "desc": event.desc,
                            "startDate": event.start, "endDate": event.end, "invitees": event.invitees,
                            "groups": event.groups, "calendar": event.calendar, "eventId": event.eventId})
        }).then((data) => data.json());
    }


    // DO LATER
    get_calendars() {
        let response = fetch('/getEvents', {
            method: 'GET'

        }).then((data) => data.json()).then(data => this.renderComponentsFromList(data));
    }

    renderComponentsFromList(calendarList) {
        //console.log(calendarList)

        var new_list = new Array()
        //console.log(calendarList.calendars)
        for (var i = 0 ; i < calendarList.calendars.length ; i++) {
                //console.log(calendarList.calendars[i])
                for (var j = 0 ; j < calendarList.calendars[i].events.length ; j++) {
                    this.setTitle(calendarList.calendars[i].events[j].title)
                    this.setDescription(calendarList.calendars[i].events[j].desc)
                    this.setInvitees(calendarList.calendars[i].events[j].invitees)
                    //setGroups(calendarList.calendars[i].events[j].groups)
                    this.setCalendar(calendarList.calendars[i].events[j].calendar)
                    this.setStart(calendarList.calendars[i].events[j].start)
                    this.setEnd(calendarList.calendars[i].events[j].end)
                    //setId(calendarList.calendars[i].events[j].eventId)

                    this.setNewEvent()

                    // var obj = [{"id":"tag1","text":"tag1"},{"id":"tag2","text":"tag2"}] ;

                    // for (var i =0; i< obj.length ;i++) {
                    //     console.log(obj[i].id);
                    // }
                    //console.log(calendarList.calendars[i].events[j])
                    //this.state.events.push(calendarList.calendars[i].events[j])
                }
        }

        this.setState((prevState) => {
            events: Array.prototype.push.apply(prevState.events, new_list)
        })

    }

    // Closes modal
    handleClose() {
        this.setState({ openEvent: false, openSlot: false });
    }
        
    //  Allows user to click on calendar slot and make new event
    handleSlotSelected(eventToEdit) {

//         to correctly store date need it in this format
        console.log(eventToEdit)
        var year = eventToEdit.start.getFullYear()
        var month = eventToEdit.start.getMonth() + 1
        console.log(month)
        var date = eventToEdit.start.getDate()


        if (month < 10) {
            month = "0" + month.toString()
        }

        if (date < 10) {
        date = "0" + date.toString()
        }

        var fullStartDate = year + "-" + month + "-" + date + "T00:00"

        var year1 = eventToEdit.start.getFullYear()
        var month1 = eventToEdit.start.getMonth() + 1
        var date1 = eventToEdit.start.getDate()


        if (month1 < 10) {
            month1 = "0" + month1.toString()
        }

        if (date1 < 10) {
        date1 = "0" + date1.toString()
        }

        var fullEndDate = year1 + "-" + month1 + "-" + date1 + "T00:00"

        console.log(eventToEdit.start);
        this.setState ({
            openSlot: true,
            title: eventToEdit.title,
            desc: eventToEdit.desc,
            start: fullStartDate,
            end: fullEndDate,
            invitees: eventToEdit.invitees,
            groups: eventToEdit.groups,
            calendar: eventToEdit.calendar,
            eventId: eventToEdit.eventId,
        });
    }
        
    //  Allows user to click on existing event
    handleEventSelected(event) {
        console.log("event", event);
        this.setState ({
            openEvent: true,
            clickedEvent: event,
            start: event.start,
            end: event.end,
            title: event.title,
            desc: event.desc,
            invitees: event.invitees,
            groups: event.groups,
            calendar: event.calendar,
            eventId: event.eventId,
        });
    }
        
    // Sets the state of events
    setTitle(e) { this.setState({ title: e }); }
    setDescription(e) { this.setState({ desc: e }); }
    setInvitees(e) { this.setState({ invitees: e }); }
    setGroups(e) { this.setState({ groups: e }); }
    setCalendar(e) { this.setState({ calendar: e }); }
    setStart(e) { this.setState({ start: e }); }
    setEnd(e) { this.setState({ end: e }); }
        
    // Handle's start time select
    handleStartTime = (event, date) => {
        this.setState({ start: date });
    };
     
    // Handle's end time select
    handleEndTime = (event, date) => {
        this.setState({ end: date });
    };

    componentDidMount() {
        this.get_calendars()
        this.render()
        this.forceUpdate()
    }
        
    // Onclick callback function that pushes new event into events array.
    setNewEvent() {
        const { title, desc, start, end, invitees, groups, calendar, eventId } = this.state;
        let event = { title, desc, start, end, invitees, groups, calendar, eventId };
        let events = this.state.events.slice();
        events.push(event);
        this.setState({ events });
        this.create_event(event)
    }
        
    // Updates Existing Event Title and/or Description
    updateEvent() {
        const { title, desc, start, end, events, invitees, groups, calendar, clickedEvent, eventId } = this.state;
        const index = events.findIndex(event => event === clickedEvent);
        const updatedEvent = events.slice();
        updatedEvent[index].title = title;
        updatedEvent[index].desc = desc;
        updatedEvent[index].start = start;
        updatedEvent[index].end = end;
        updatedEvent[index].invitees = invitees;
        updatedEvent[index].groups = groups;
        updatedEvent[index].calendar = calendar;
        updatedEvent[index].eventId = eventId;
        this.setState({
            events: updatedEvent
        });
        this.edit_event(updatedEvent[index])
    }
        
    // Filters out specific event that is to be deleted and set that variable to state
    deleteEvent() {
        let updatedEvents = this.state.events.filter (
            event => event["eventId"] !== this.state.eventId
        );

        let deletedEvent = this.state.events.filter (
            event => event["eventId"] === this.state.eventId
        )
        console.log(updatedEvents)
        console.log(deletedEvent)
        this.setState({ events: updatedEvents });
        this.delete_event(deletedEvent[0])
    }

    render() {
        const { classes } = this.props;
        return (
            <div className={classes.root} >
            <CssBaseline />
            <Navbar/>
            <main className={classes.content}>
                <div className={classes.toolbar} />
                <Calendar className={classes.calendar}
                //onLoad={console.log('LOADED')}
                  selectable
                  popup
                  localizer = {localizer}
                  defaultDate = {new Date()}
                  defaultView = "month"
                  events = {this.state.events}
                  showMultiDayTimes = {true}
                  onSelectSlot = {slotInfo => this.handleSlotSelected(slotInfo)}
                  onSelectEvent = {event => this.handleEventSelected(event)}
                //   components={{
                //     event: Event
                //   }}
                />
                {/* Modal for booking new event */}
                <Dialog open={this.state.openSlot} onClose={this.handleClose}>
                  <DialogContent>
                    <TextField className={classes.title}
                    inputProps={{
                        style: {fontSize: 23} 
                    }}
                    placeholder="Add title"
                    fullWidth
                    autoFocus
                    margin="dense"
                    onChange={e => {
                      this.setTitle(e.target.value);
                    }}
                    />
                    <br />
                    <TextField 
                    className={classes.inputMargin}
                    fullWidth
                    placeholder="Add description"
                    margin="dense"
                    onChange={e => {
                      this.setDescription(e.target.value);
                    }}
                    />
                    <TextField 
                    className={classes.inputMargin}
                    type="datetime-local"
                    defaultValue={this.state.start}
                    onChange={e => {
                        this.setStart(e.target.value), this.handleStartTime;
                    }}
                    />
                    <TextField 
                    className={classes.inputMargin}
                    type="datetime-local"
                    value={this.state.end}
                    onChange={e => {
                        this.setEnd(e.target.value), this.handleEndTime;
                    }}
                    />
                    <TextField 
                    className={classes.inputMargin}
                    placeholder="Add invitees"
                    margin="dense"
                    onChange={e => {
                        this.setInvitees(e.target.value);
                    }}
                    />
                    <TextField 
                    className={classes.inputMargin}
                    placeholder="Add group invitees"
                    margin="dense"
                    onChange={e => {
                        this.setGroups(e.target.value);
                    }}
                    /> 
                    <InputLabel htmlFor="demo-dialog-native">Calendar</InputLabel>
                    <Select
                      native
                      value={this.state.calendar}
                      defaultValue='Default'
                      onChange={e => {
                        this.setCalendar(e.target.value);
                      }}
                    >
                        <option value="" />
                        <option value={"Default"}>Default</option>
                        <option value={"Work"}>Work</option>
                        <option value={"Social"}>Social</option>
                    </Select>                   
                  </DialogContent>
                  <DialogActions>
                    <Button 
                    label="Cancel" 
                    color="primary"
                    onClick={this.handleClose} 
                    >
                    Cancel
                    </Button>
                    <Button
                    label="Submit"
                    variant="contained" 
                    color="primary"
                    onClick={() => {
                      this.setNewEvent(), this.handleClose();
                    }}
                    >
                    Submit
                    </Button>
                  </DialogActions>
                </Dialog>

                {/* Material-ui Modal for Existing Event */}
                <Dialog open={this.state.openEvent} onClose={this.handleClose}>
                  <DialogContent>
                    <TextField 
                    className={classes.title}
                    inputProps={{
                        style: {fontSize: 23} 
                    }}
                    placeholder="Add title"
                    fullWidth
                    autoFocus
                    margin="dense"
                    defaultValue={this.state.title}
                    onChange={e => {
                      this.setTitle(e.target.value);
                    }}
                    />
                    <br />
                    <TextField
                    className={classes.inputMargin}
                    fullWidth
                    placeholder="Add description"
                    margin="dense"
                    multiline={true}
                    defaultValue={this.state.desc}
                    onChange={e => {
                      this.setDescription(e.target.value);
                    }}
                    />
                    <TextField
                    className={classes.inputMargin}
                    type="datetime-local"
                    value={this.state.start}
                    onChange={e => {
                        this.setStart(e.target.value);
                    }}
                    />
                    <TextField
                    className={classes.inputMargin}
                    type="datetime-local"
                    defaultValue={this.state.end}
                    onChange={e => {
                        this.setEnd(e.target.value);
                    }}
                    />
                    <TextField
                    className={classes.inputMargin}
                    defaultValue={this.state.invitees}
                    placeholder="Add invitees"
                    margin="dense"
                    onChange={e => {
                        this.setInvitees(e.target.value);
                    }}
                    />
                    <TextField
                    className={classes.inputMargin}
                    defaultValue={this.state.group}
                    placeholder="Add group invitees"
                    margin="dense"
                    onChange={e => {
                        this.setGroup(e.target.value);
                    }}
                    /> 
                    <InputLabel htmlFor="demo-dialog-native">Calendar</InputLabel>
                    <Select
                      native
                      value={this.state.calendar}
                      defaultValue='Default'
                      onChange={e => {
                        this.setCalendar(e.target.value);
                      }}
                    >
                        <option value="" />
                        <option value={"Default"}>Default</option>
                        <option value={"Work"}>Work</option>
                        <option value={"Social"}>Social</option>
                    </Select> 
                  </DialogContent>
                  <DialogActions>
                    <Button 
                    label="Cancel" 
                    color="primary"
                    onClick={this.handleClose} 
                    >
                    Cancel
                    </Button>
                    <Button
                    label="Delete"
                    variant="contained" 
                    color="primary"
                    onClick={() => {
                      this.deleteEvent(), this.handleClose();
                    }}
                    >
                    Delete
                    </Button>
                    <Button
                    label="Edit"
                    variant="contained" 
                    color="primary"
                    onClick={() => {
                      this.updateEvent(), this.handleClose();
                    }}
                    >
                    Edit
                    </Button>
                  </DialogActions>
                </Dialog>
            </main>
            <Sidebar />
            </div>
        );
    }
}

function Event({ event }) {
    // let popoverClickRootClose = (
    //   <Popover id="popover-trigger-click-root-close" style={{ zIndex: 10000 }}>
    //     <strong>Holy guacamole!</strong> Check this info.
    //     <strong>{event.title}</strong>
    //   </Popover>
    // );
  
    console.log(event);
    return (
      <div>
        <div>{event.start.getHours().toString()}</div>
        <div>{event.title}</div>
        
      </div>
    );
  }

export default withStyles(styles)(Cal);

// eventStyleGetter: function(event, start, end, isSelected) {
//     console.log(event);
//     var backgroundColor = '#' + event.hexColor;
//     var style = {
//         backgroundColor: backgroundColor,
//         borderRadius: '0px',
//         opacity: 0.8,
//         color: 'black',
//         border: '0px',
//         display: 'block'
//     };
//     return {
//         style: style
//     };
// },

// getEventStyle(event, start, end, isSelected) {
//     const style = {}
//     const todayDate = new Date().getDate()

//     if (start.getDate() === todayDate) {
//       style.backgroundColor = 'green'
//     } else if (start.getDate() < todayDate) {
//       style.backgroundColor = 'red'
//     } else if (start.getDate() > todayDate) {
//       style.backgroundColor = 'blue'
//     }
//     if (event.bgcolor) {
//       style.backgroundColor = event.bgcolor
//     }

//     return { style }
//   }


                  // UNCOMMENT LATER TO COLOUR DIFF EVENTS
                  //eventPropGetter={(this.eventStyleGetter)}
                //   eventPropGetter={event => ({
                //     style: {
                //       backgroundColor: event.color,
                //     },
                //   })}