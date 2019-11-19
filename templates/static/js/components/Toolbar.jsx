class CustomToolbar extends React.Component {
    render() {
        let { localizer: { messages }, label } = this.props
        return(
            <div className="rbc-toolbar">
                {/* Arrows */}
                <NavigateBeforeIcon type="button" onClick={this.navigate.bind(null, navigate.PREVIOUS)}/>
                <p type="button" onClick={this.navigate.bind(null, navigate.TODAY)}>Today</p>
                <NavigateNextIcon type="button" onClick={this.navigate.bind(null, navigate.NEXT)}/>
                {/* Title */}
                <span className="rbc-toolbar-label">{label}</span>
                {/* Views */}
                <div className="rbc-btn-group">
					<button type="button" onClick={this.view.bind(null, 'month')}>Month</button>
					<button type="button" onClick={this.view.bind(null, 'week')}>Week</button>
					<button type="button" onClick={this.view.bind(null, 'day')}>Day</button>
					<button type="button" onClick={this.view.bind(null, 'agenda')}>Agenda</button>
				</div>
            </div>
        )
    }
    navigate = action => {
        this.props.onNavigate(action)
    }
    view = action => {
        this.props.onView(action);
    }
}

export let navigate = {
    PREVIOUS: 'PREV',
    NEXT: 'NEXT',
    TODAY: 'TODAY',
    DATE: 'DATE',
}