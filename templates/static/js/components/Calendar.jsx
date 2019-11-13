import React, { Component } from "react";
import { Calendar, momentLocalizer} from 'react-big-calendar';
import { Dialog, DialogActions, DialogContent, Button, TextField } from "@material-ui/core";
import moment from "moment";
import Navbar from './Navbar'
import Sidebar from './Sidebar'
import Select from '@material-ui/core/Select';
import CssBaseline from '@material-ui/core/CssBaseline';
import "!style-loader!css-loader!react-big-calendar/lib/css/react-big-calendar.css";
import { withStyles } from "@material-ui/core/styles";

// Initialise time localiser
const localizer = momentLocalizer(moment)

const drawerWidth = 300;

const styles = theme => ({
    calendar: {
        height: "85vh", 
        position: "fixed", 
        width: "1120px",
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
});


// Load events
class Cal extends Component {  
    constructor() {
        super();
        this.state = {
            // Loading sample events, remove later
            events: [  
              {
                id: 0,
                title: 'All Day Event very long title',
                allDay: true,
                start: new Date(2019, 10, 27, 2, 0, 0),
                end: new Date(2019, 10, 27, 4, 0, 0),
              },
              {
                id: 1,
                title: 'Long Event',
                start: new Date(2019, 10, 5, 8, 0, 0),
                end: new Date(2019, 10, 8, 9, 0, 0),
              },
              {
                id: 2,
                title: 'Hawaii',
                start: new Date(2019, 10, 18, 12, 0, 0),
                end: new Date(2019, 10, 18, 2, 0, 0),
              },
              {
                id: 3,
                title: 'Party',
                start: new Date(2019, 10, 5, 5, 0, 0),
                end: new Date(2019, 10, 5, 12, 0, 0),
              },  
              {
                id: 4,
                title: 'Conference',
                start: new Date(2019, 10, 8, 4, 0, 0),
                end: new Date(2019, 10, 8, 12, 0, 0),
                desc: 'Big conference for important people',
              },
              {
                id: 5,
                title: 'Double Event',
                start: new Date(2019, 10, 8, 12, 0, 0),
                end: new Date(2019, 10, 8, 1, 0, 0),
              },
              {
                id: 6,
                title: 'Triple Event',
                start: new Date(2019, 10, 8, 1, 0, 0),
                end: new Date(2019, 10, 8, 3, 0, 0),
              },
              {
                id: 7,
                title: '4 Event',
                start: new Date(2019, 10, 8, 2, 0, 0),
                end: new Date(2019, 10, 8, 5, 0, 0),
              },
              {
                id: 8,
                title: '5 Event',
                start: new Date(2019, 10, 8, 3, 0, 0),
                end: new Date(2019, 10, 8, 8, 0, 0),
              },
            ],
            title: "",
            start: "",
            end: "",
            desc: "",
            openSlot: false,
            openEvent: false,
            clickedEvent: {},
        };
        this.handleClose = this.handleClose.bind(this);
    };

    create_event(event) {
        console.log(event)
        // console.log(event.state)
        console.log(JSON.stringify({"name": event.title, "desc": event.desc, 
                                    "startDate": event.start, "endDate": event.end, "invitees": event.invitees,
                                    "groups": event.groups, "cal": event.cal}))
        let response = fetch('/createEvent', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8'
            },
        body: JSON.stringify({"name": event.title, "desc": event.desc, 
                            "startDate": event.start, "endDate": event.end, "invitees": event.invitees,
                            "groups": event.groups, "cal": event.cal})
        }).then((data) => data.json()).then(event => {
            console.log(event)
            if (event.status === 200) {
                // append to events list
                console.log("Created event successfully", event.responseText)
                events.push(event)
            } else {
                console.log("Failed event creation", event.responseText)
            }
        });
    }

    edit_event(event) {
        console.log(JSON.stringify({"name": event.title, "desc": event.desc, 
                                    "startDate": event.start, "endDate": event.end, "invitees": event.invitees,
                                    "groups": event.groups, "cal": event.cal}))
        let response = fetch('/createEvent', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8'
            },
        body: JSON.stringify({"name": event.title, "desc": event.desc, 
                            "startDate": event.start, "endDate": event.end, "invitees": event.invitees,
                            "groups": event.groups, "cal": event.cal})
        }).then((data) => data.json()).then(event => editEvent(event));
    }

    // DO LATER
    get_calendars() {
        let response = fetch('/getEvents', {
            method: 'POST'

        }).then((data) => data.json()).then(calendarList => renderComponentsFromList(calendarList));
    }

    // DO LATER
    get_events_by_calendar() {
        let response = fetch('/getEvents', {
            method: 'POST'

        }).then((data) => data.json()).then(calendarList => renderComponentsFromList(calendarList));
    }

    handleClose() {
        this.setState({ openEvent: false, openSlot: false });
    }
        
    //  Allows user to click on calendar slot and handles if event exists
    handleSlotSelected(eventToEdit) {
        console.log("Edit calendar info", eventToEdit);
        this.setState ({
            openSlot: true,
            title: eventToEdit.title,
            desc: eventToEdit.desc,
            start: eventToEdit.start,
            end: eventToEdit.end,
            invitees: eventToEdit.invitees,
            groups: eventToEdit.groups,
        });
    }
        
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
        });
    }
        
    setTitle(e) {
        this.setState({ title: e });
    }
        
    setDescription(e) {
        this.setState({ desc: e });
    }

    setInvitees(e) {
        this.setState({ invitees: e });
    }

    setGroup(e) {
        this.setState({ group: e });
    }

    setStart(e) {
        this.setState({ start: e });
    }

    setEnd(e) {
        this.setState({ end: e });
    }
        
    handleStartTime = (event, date) => {
        this.setState({ start: date });
    };
        
    handleEndTime = (event, date) => {
        this.setState({ end: date });
    };
        
    // Onclick callback function that pushes new event into events array.
    setNewEvent() {
        const { start, end, title, desc, invitees, groups } = this.state;
        let event = { title, start, end, desc, invitees, groups };
        let events = this.state.events.slice();
        events.push(event);
        this.setState({ events });
        this.create_event(event)
    }
        
    //  Updates Existing Event Title and/or Description
    updateEvent() {
        const { title, desc, start, end, events, invitees, groups, clickedEvent } = this.state;
        const index = events.findIndex(event => event === clickedEvent);
        const updatedEvent = events.slice();
        updatedEvent[index].title = title;
        updatedEvent[index].desc = desc;
        updatedEvent[index].start = start;
        updatedEvent[index].end = end;
        updatedEvent[index].invitees = invitees;
        updatedEvent[index].groups = groups;
        this.setState({
            events: updatedEvent
        });
        this.edit_event(updatedEvent)
    }
        
    //  filters out specific event that is to be deleted and set that variable to state
    deleteEvent() {
        let updatedEvents = this.state.events.filter (
            event => event["start"] !== this.state.start
        );
        // localStorage.setItem("cachedEvents", JSON.stringify(updatedEvents));
        this.setState({ events: updatedEvents });
    }

    render() {
        const { classes } = this.props;
        return (
            <div className={classes.root}>
            <CssBaseline />
            <Navbar className={classes.appBar}/>

            <main className={classes.content}>
                <div className={classes.toolbar} />
                <Calendar className={classes.calendar}
                  selectable
                  popup
                  localizer = {localizer}
                  defaultDate = {new Date()}
                  defaultView = "month"
                  events = {this.state.events}
                  showMultiDayTimes={true}
                  onSelectSlot = {slotInfo => this.handleSlotSelected(slotInfo)}
                  onSelectEvent = {event => this.handleEventSelected(event)}

                  // UNCOMMENT LATER TO COLOUR DIFF EVENTS
                  //eventPropGetter={(this.eventStyleGetter)}
                //   eventPropGetter={event => ({
                //     style: {
                //       backgroundColor: event.color,
                //     },
                //   })}
                />

                {/* Modal for booking new event */}
                <Dialog open={this.state.openSlot} onClose={this.handleClose}>
                  <DialogContent>
                    <TextField
                    label="Title"
                    onChange={e => {
                      this.setTitle(e.target.value);
                    }}
                    />
                    <br />
                    <TextField
                    label="Description"
                    onChange={e => {
                      this.setDescription(e.target.value);
                    }}
                    />
                    <TextField
                    type="datetime-local"
                    value={this.state.start}
                    onChange={e => {
                        this.setStart(e.target.value), this.handleStartTime;
                    }}
                    />
                    <TextField
                    type="datetime-local"
                    value={this.state.end}
                    onChange={e => {
                        this.setEnd(e.target.value), this.handleEndTime;
                    }}
                    />
                    <TextField
                    label="Invitees"
                    onChange={e => {
                        this.setInvitees(e.target.value);
                    }}
                    />
                    <TextField
                    label="Groups"
                    onChange={e => {
                        this.setGroup(e.target.value);
                    }}
                    /> 
                    <Select
                      native
                    //   onChange={e => {
                    //     this.setCalendar(e.)
                    //   }}
                    //   value={}
                    //   onChange={handleChange('age')}
                    //   inputProps={{
                    //     name: 'age',
                    //     id: 'age-native-simple',
                    //   }}
                    >
                        <option value="" />
                        <option value={10}>Default</option>
                        <option value={20}>Work</option>
                        <option value={30}>Social</option>
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
                    defaultValue={this.state.title}
                    label="Title"
                    onChange={e => {
                      this.setTitle(e.target.value);
                    }}
                    />
                    <br />
                    <TextField
                    label="Description"
                    multiline={true}
                    defaultValue={this.state.desc}
                    onChange={e => {
                      this.setDescription(e.target.value);
                    }}
                    />
                    <TextField
                    type="datetime-local"
                    defaultValue={this.state.start}
                    onChange={e => {
                        this.setStart(e.target.value), this.handleStartTime;
                    }}
                    />
                    <TextField
                    type="datetime-local"
                    defaultValue={this.state.end}
                    onChange={e => {
                        this.setEnd(e.target.value), this.handleEndTime;
                    }}
                    />
                    <TextField
                    defaultValue={this.state.invitees}
                    label="Invitees"
                    onChange={e => {
                        this.setInvitees(e.target.value);
                    }}
                    />
                    <TextField
                    defaultValue={this.state.group}
                    label="Groups"
                    onChange={e => {
                        this.setGroup(e.target.value);
                    }}
                    />  
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
                    label="Submit"
                    variant="contained" 
                    color="primary"
                    onClick={() => {
                      this.updateEvent(), this.handleClose();
                    }}
                    >
                    Submit
                    </Button>
                  </DialogActions>
                </Dialog>
            </main>
            <Sidebar />
            </div>
        );
    }
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


