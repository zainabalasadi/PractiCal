import React, { Component } from "react";
import { Calendar, momentLocalizer} from 'react-big-calendar';
import moment from "moment";
import "!style-loader!css-loader!../../../public/css/calendar.css";
import "!style-loader!css-loader!react-big-calendar/lib/css/react-big-calendar.css";

const localizer = momentLocalizer(moment)
  
class Cal extends Component {
    state = {
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
        ]
    };

    render() {
        return (
            <div className="App">
                <Calendar
                    localizer={localizer}
                    defaultDate={new Date()}
                    defaultView="month"
                    events={this.state.events}
                    style={{ height: "100vh" }}
                />
            </div>
        );
    }
}

export default Cal;