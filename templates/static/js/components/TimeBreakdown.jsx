import React, { Component } from "react";
import Button from '@material-ui/core/Button';
import { Dialog, DialogContent, DialogContentText, DialogTitle } from '@material-ui/core';
import CloseIcon from '@material-ui/icons/Close';
import IconButton from '@material-ui/core/IconButton';
import { withStyles } from "@material-ui/core/styles";
import TimelineIcon from '@material-ui/icons/Timeline';

const styles = theme => ({
    closeButton: {
        position: 'absolute',
        right: theme.spacing(1),
        top: theme.spacing(1),
    },
    heading: {
        fontSize: 100,
        margin: '20px 0 10px 0',
    }
});

class TimeBreakdown extends Component {
    _isMounted = false;
    constructor() {
        super();
        this.state = {
            // Loading sample events, remove later
            open: false,
            setOpen: false,
            userName: "",
            breakdown: [],
            family: "",
            social: "",
            school: "",
            work: "",
            greeting: "",
        };
        this.handleClose = this.handleClose.bind(this);
        this.getHours = this.getHours.bind(this);
        this.handleClickOpen = this.handleClickOpen.bind(this);
        this.getGreeting = this.getGreeting.bind(this);
    };

    componentDidMount() {
        this._isMounted = true;
        
        // Assign greeting
        var now = new Date(),
            hour = now.getHours();

        if (hour > 12) {
            this.setState({ greeting: "Good afternoon"})
        } else {
            this.setState({ greeting: "Good morning"})
        }
      
        let response = fetch('/getName', {
            method: 'GET'

        }).then((data) => data.json()).then(result => {
            if (this._isMounted) {
                this.setState({userName: result})
            }
        });
    }
    
    componentWillUnmount() {
        this._isMounted = false;
    }

    handleClickOpen() {
        this.setState({ setOpen: true });
        this.getHours()
    }

    // Closes modal
    handleClose() {
        this.setState({ setOpen: false });
    }

    getHours() {
        let response = fetch('/getCategoryHours', {
            method: 'GET'

        }).then((data) => data.json()).then(data => this.renderHours(data));//then(data => this.setState({ breakdown: data }));
    }

    renderHours(data) {
        this.setState({ social: data['Social'] });
        this.setState({ family: data['Family'] });
        this.setState({ school: data['School'] });
        this.setState({ work: data['Work'] });
        this.setState({ misc: data['Miscellaneous'] });
        console.log(this.state.social)
    }

    getGreeting() {

    }

    render() {
        const { classes } = this.props;
        return (
        <div>
            <IconButton color="inherit" onClick={this.handleClickOpen}>
                <TimelineIcon />
            </IconButton>
            <Dialog
            maxWidth = {'md'}
            open={this.state.setOpen}
            onClose={this.handleClose}
            aria-labelledby="alert-dialog-title"
            aria-describedby="alert-dialog-description"
            >
                <IconButton aria-label="close" className={classes.closeButton} onClick={this.handleClose}>
                    <CloseIcon />
                </IconButton>
                <DialogTitle className={classes.heading}>
                    {`${this.state.greeting} ${this.state.userName},`}
                </DialogTitle>
                <DialogContent>
                    <DialogContentText>
                    <p className="timeIntro">Last week, you spent:</p>
                    <div className="inline social tiles">
                        <p className="timeNum">{this.state.social}<span>hours</span></p>
                        <p className="timeType">on social events</p>                    
                    </div>
                    <div className="inline work tiles">
                        <p className="timeNum">{this.state.work}<span>hours</span></p>
                        <p className="timeType">on work events</p>                    
                    </div>
                    <div className="inline school tiles">
                        <p className="timeNum">{this.state.school}<span>hours</span></p>
                        <p className="timeType">on school events</p>                    
                    </div>
                    <div className="inline family tiles">
                        <p className="timeNum">{this.state.family}<span>hours</span></p>
                        <p className="timeType">on family events</p>                    
                    </div>
                    <div className="inline misc tiles">
                        <p className="timeNum">{this.state.misc}<span>hours</span></p>
                        <p className="timeType">on miscellaneous events</p>                    
                    </div>
                    </DialogContentText>
                </DialogContent>
            </Dialog>
        </div>
        );
    }
}

export default withStyles(styles)(TimeBreakdown);