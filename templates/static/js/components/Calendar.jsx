import React, { Component } from 'react'
import BigCalendar from 'react-big-calendar'
import 'react-big-calendar/lib/css/react-big-calendar.css'
import "react-big-calendar/lib/addons/dragAndDrop/styles.css"
import moment from 'moment'
import Modal from './Modal'
import events from './events'
// import './index.css'

moment.locale(navigator.language, {
  week: {
    dow: 1
  },
});

const localizer = BigCalendar.momentLocalizer(moment)
const formats = {
  timeGutterFormat: 'H:mm',
  agendaTimeFormat: 'H:mm',
  agendaHeaderFormat: ({ start, end }, culture, local) => (
    `${local.format(start, "MMMM D")} — ${local.format(end, "MMMM D")}`),
  dayHeaderFormat: 'dddd MMMM Do',
}
const DragAndDropCalendar = withDragAndDrop(BigCalendar)

export default class Calendar extends Component {
  constructor() {
    super()
    this.state = {
      events: events,
      modalIsOpen: false,
      isNewEvent: false,
      modalEvent: {
        title: '',
        start: null,
        end: null,
        desc: '',
        id: null
      },
    }
  }

  selectSlot = (event) => {
    this.setState({ isNewEvent: true })
    event.start = event.slots[0]
    event.end = event.slots[event.slots.length - 1]
    this.openModal(event)
  }

  selectEvent = (event) => {
    this.setState({ isNewEvent: false })
    this.openModal(event)
  }

  openModal = (event) => {
    const id = event.id ? event.id : Date.now()
    this.setState({
      modalIsOpen: true,
      modalEvent: {
        ...event,
        id
      }
    });
  }

  getEventStyle(event, start, end, isSelected) {
    const style = {}
    const todayDate = new Date().getDate()

    if (start.getDate() === todayDate) {
      style.backgroundColor = 'green'
    } else if (start.getDate() < todayDate) {
      style.backgroundColor = 'red'
    } else if (start.getDate() > todayDate) {
      style.backgroundColor = 'blue'
    }
    if (event.bgcolor) {
      style.backgroundColor = event.bgcolor
    }

    return { style }
  }

  closeModal = () => {
    this.setState({ modalIsOpen: false });
  }

  handleModalEventEdit = (key, newValue) => {
    const newData = { ...this.state.modalEvent }
    newData[key] = newValue
    this.setState({
      modalEvent: newData
    })
  }

  handleEventSave = (newEvent) => {
    const index = this.state.events.findIndex( event => event.id === newEvent.id )
    if (index > -1) {
      const newEvents = this.state.events
      newEvents[index] = { ...newEvent }
      this.setState({
        events: newEvents
      })
    } else {
      this.setState({
        events: [
          ...this.state.events,
          { ...newEvent },
        ],
      })
    }
  }

  handleEventDelete = () => {
    const index = this.state.events.findIndex(event => {
      return event.id === this.state.modalEvent.id
    })
    if (index > -1) {
      const newEvents = this.state.events
      newEvents.splice(index, 1)
      this.setState({
        events: newEvents
      })
    }
  }

  render() {
    return (
      <>
        <DragAndDropCalendar style={{ height: '100vh' }}
          localizer={localizer}
          formats={formats}
          events={this.state.events}
          defaultView={'month'}
          defaultDate={new Date()}  // onSelectEvent click doesn't fire without this
          min={moment('10:00am', 'H:mma').toDate()}
          max={moment('09:59pm', 'H:mma').toDate()}
          step={60}
          showMultiDayTimes={true}
          selectable={true}
          onSelectEvent={this.selectEvent}
          onSelectSlot={this.selectSlot}
          popup={true}
          tooltipAccessor={(e) => e.title}
          eventPropGetter={this.getEventStyle}
        />
        <Modal 
          modalIsOpen={this.state.modalIsOpen}
          closeModal={this.closeModal}
          handleModalEventEdit={this.handleModalEventEdit}
          modalEvent={this.state.modalEvent}
          handleEventSave={this.handleEventSave}
          handleEventDelete={this.handleEventDelete}
          isNewEvent={this.state.isNewEvent}
          key={this.state.modalEvent.id}
        />
      </>
    )
  }
}