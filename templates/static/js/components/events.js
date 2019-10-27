const thisMonth = new Date().getMonth()

export default [
  {
    id: 1,
    title: 'All Day Event very long title',
    allDay: true,
    start: new Date(2019, thisMonth, 1, 0),
    end: new Date(2019, thisMonth, 1, 24),
  },
  {
    id: 4,
    title: 'Some Event',
    start: new Date(2019, thisMonth, 9, 0, 0, 0),
    end: new Date(2019, thisMonth, 10, 0, 0, 0),
  },
  {
    id: 5,
    title: 'Conference',
    start: new Date(2019, thisMonth, 11),
    end: new Date(2019, thisMonth, 13),
    desc: 'Big conference for important people',
  },
  {
    id: 6,
    title: 'Meeting',
    start: new Date(2019, thisMonth, 12, 10, 30, 0, 0),
    end: new Date(2019, thisMonth, 12, 12, 30, 0, 0),
    desc: 'Pre-meeting meeting, to prepare for the meeting',
  },
  {
    id: 7,
    title: 'Lunch',
    start: new Date(2019, thisMonth, 12, 12, 0, 0, 0),
    end: new Date(2019, thisMonth, 12, 13, 0, 0, 0),
    desc: 'Power lunch',
  },
  {
    id: 8,
    title: 'Meeting',
    start: new Date(2019, thisMonth, 12, 14, 0, 0, 0),
    end: new Date(2019, thisMonth, 12, 15, 0, 0, 0),
  },
  {
    id: 9,
    title: 'Happy Hour',
    start: new Date(2019, thisMonth, 12, 17, 0, 0, 0),
    end: new Date(2019, thisMonth, 12, 17, 30, 0, 0),
    desc: 'Most important meal of the day',
  },
  {
    id: 10,
    title: 'Dinner',
    start: new Date(2019, thisMonth, 12, 20, 0, 0, 0),
    end: new Date(2019, thisMonth, 12, 21, 0, 0, 0),
  },
  {
    id: 11,
    title: 'Birthday Party',
    start: new Date(2019, thisMonth, 13, 7, 0, 0),
    end: new Date(2019, thisMonth, 13, 10, 30, 0),
  },
  {
    id: 12,
    title: 'Late Night Event',
    start: new Date(2019, thisMonth, 17, 19, 30, 0),
    end: new Date(2019, thisMonth, 18, 2, 0, 0),
  },
  {
    id: 12.5,
    title: 'Late Same Night Event',
    start: new Date(2019, thisMonth, 17, 19, 30, 0),
    end: new Date(2019, thisMonth, 17, 23, 30, 0),
  },
  {
    id: 13,
    title: 'Multi-day Event',
    start: new Date(2019, thisMonth, 20, 19, 30, 0),
    end: new Date(2019, thisMonth, 22, 2, 0, 0),
    bgcolor: 'purple',    
  },
  {
    id: 14,
    title: 'Today',
    start: new Date(new Date().setHours(16)),
    end: new Date(new Date().setHours(18)),
  },
]