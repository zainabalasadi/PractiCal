import React, { Component } from "react";
import { Calendar, momentLocalizer} from 'react-big-calendar';
import { Dialog, DialogActions, DialogContent, Button, TextField } from "@material-ui/core";
import moment from "moment";

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
            clickedEvent: {}
        };
        this.handleClose = this.handleClose.bind(this);
    };

    handleClose() {
        this.setState({ openEvent: false, openSlot: false });
    }
        
    //  Allows user to click on calendar slot and handles if appointment exists
    handleSlotSelected(slotInfo) {
        console.log("Real slotInfo", slotInfo);
        this.setState ({
            openSlot: true,
            title: "",
            desc: "",
            start: slotInfo.start,
            end: slotInfo.end
            
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
            desc: event.desc
        });
    }
        
    setTitle(e) {
        this.setState({ title: e });
    }
        
    setDescription(e) {
        this.setState({ desc: e });
    }
        
    handleStartTime = (event, date) => {
        this.setState({ start: date });
    };
        
    handleEndTime = (event, date) => {
        this.setState({ end: date });
    };
        
    // Onclick callback function that pushes new appointment into events array.
    setNewAppointment() {
        const { start, end, title, desc } = this.state;
        let appointment = { title, start, end, desc };
        let events = this.state.events.slice();
        events.push(appointment);
        // localStorage.setItem("cachedEvents", JSON.stringify(events));
        this.setState({ events });
    }
        
    //  Updates Existing Appointments Title and/or Description
    updateEvent() {
        const { title, desc, start, end, events, clickedEvent } = this.state;
        const index = events.findIndex(event => event === clickedEvent);
        const updatedEvent = events.slice();
        updatedEvent[index].title = title;
        updatedEvent[index].desc = desc;
        updatedEvent[index].start = start;
        updatedEvent[index].end = end;
        // localStorage.setItem("cachedEvents", JSON.stringify(updatedEvent));
        this.setState({
            events: updatedEvent
        });
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
        return (
            <div className="App">
                <Calendar
                    selectable
                    popup
                    localizer = {localizer}
                    defaultDate = {new Date()}
                    defaultView = "month"
                    events = {this.state.events}
                    onSelectSlot = {slotInfo => this.handleSlotSelected(slotInfo)}
                    onSelectEvent = {event => this.handleEventSelected(event)}
                    style = {{ height: "100vh" }}
                />

                {/* Modal for booking new appointment */}
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
                          onChange={this.handleStartTime}
                        />
                        <TextField
                          type="datetime-local"
                          value={this.state.end}
                          onChange={this.handleEndTime}
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
                          multiLine={true}
                          defaultValue={this.state.desc}
                          onChange={e => {
                            this.setDescription(e.target.value);
                          }}
                        />
                        <TextField
                          type="datetime-local"
                          defaultValue={this.state.start}
                          onChange={this.handleStartTime}
                        />
                        <TextField
                          type="datetime-local"
                          defaultValue={this.state.end}
                          onChange={this.handleEndTime}
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
        );
    }
}

export default Cal;