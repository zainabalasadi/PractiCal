import React, { Component } from "react";
import { Calendar, momentLocalizer} from 'react-big-calendar';
import { Dialog, DialogActions, Typography, DialogContent, Button, TextField } from "@material-ui/core";
import moment from "moment";
import Drawer from '@material-ui/core/Drawer';
import Navbar from './Navbar'
import "!style-loader!css-loader!react-big-calendar/lib/css/react-big-calendar.css";

// Initialise time localiser
const localizer = momentLocalizer(moment)

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
                start: new Date(2019, 9, 27),
                end: new Date(2018, 9, 27),
              },
              {
                id: 1,
                title: 'Long Event',
                start: new Date(2019, 9, 20),
                end: new Date(2019, 9, 23),
              },
              {
                id: 2,
                title: 'Hawaii',
                start: new Date(2019, 9, 18, 0, 0, 0),
                end: new Date(2019, 9, 18, 0, 0, 0),
              },
              {
                id: 3,
                title: 'Party',
                start: new Date(2019, 10, 5, 0, 0, 0),
                end: new Date(2019, 10, 5, 0, 0, 0),
              },  
              {
                id: 4,
                title: 'Conference',
                start: new Date(2019, 9, 5),
                end: new Date(2019, 9, 5),
                desc: 'Big conference for important people',
              },
              {
                id: 5,
                title: 'Double Event',
                start: new Date(2019, 9, 20),
                end: new Date(2019, 9, 20),
              },
              {
                id: 6,
                title: 'Triple Event',
                start: new Date(2019, 9, 20),
                end: new Date(2019, 9, 20),
              },
              {
                id: 7,
                title: '4 Event',
                start: new Date(2019, 9, 20),
                end: new Date(2019, 9, 20),
              },
              {
                id: 8,
                title: '5 Event',
                start: new Date(2019, 9, 20),
                end: new Date(2019, 9, 20),
              },
            ],
            title: "",
            start: "",
            end: "",
            desc: "",
            openSlot: false,
            openEvent: false,
            clickedEvent: {},
            search: ""
        };
        this.handleClose = this.handleClose.bind(this);
        this.handleSearch = this.handleSearch.bind(this);
    };

    create_event(event) {
        console.log(event.state)
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
        }).then((data) => data.json()).then(event => createEvent(event));
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
        
    //  Allows user to click on calendar slot and handles if appointment exists
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
        console.log(e);
        this.setState({ title: e });
    }
        
    setDescription(e) {
        this.setState({ desc: e });
        console.log(e);
    }

    setInvitees(e) {
        this.setState({ invitees: e });
    }

    setGroup(e) {
        this.setState({ group: e });
    }

    setStart(e) {
        this.setState({ start: e });
        console.log(e);
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
        
    // Onclick callback function that pushes new appointment into events array.
    setNewAppointment() {
        const { start, end, title, desc, invitees, groups } = this.state;
        let appointment = { title, start, end, desc, invitees, groups };
        let events = this.state.events.slice();
        events.push(appointment);
        this.setState({ events });
        this.create_event(appointment)
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

    // handle search bar
    handleSearch(event) {
      const {name, value} = event.target
      this.setState({ [name]: value})
      console.log(this.state.search)
    }

    render() {
        return (
          <div className="">
            <Navbar />
            <main className="cal-content">
              <div className="App" style = {{ position: "relative" }}>
                <Calendar
                  selectable
                  popup
                  localizer = {localizer}
                  defaultDate = {new Date()}
                  defaultView = "month"
                  events = {this.state.events}
                  onSelectSlot = {slotInfo => this.handleSlotSelected(slotInfo)}
                  onSelectEvent = {event => this.handleEventSelected(event)}
                  style = {{ height: "85vh", padding: "50px" }}
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
                      this.setNewAppointment(), this.handleClose();
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
              </div>
            </main>

				<Drawer
				className="draw"
				variant="permanent"
				anchor="right"
				classes={{
				  paper: 'draw-paper',
				}}
				>
					<Typography>
						Sidebar here
					</Typography>
				</Drawer>
			</div>
            
        );
    }
}

export default Cal;