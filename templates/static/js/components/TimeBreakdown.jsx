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
        margin: '20px 0 20px 0',
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
            family:"",
            social:"",
            school:"",
            work:"",
        };
        this.handleClose = this.handleClose.bind(this);
        this.getHours = this.getHours.bind(this);
        this.handleClickOpen = this.handleClickOpen.bind(this);
    };

    componentDidMount() {
        this._isMounted = true;
      
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
        console.log(this.state.social)
    }

    render() {
        const { classes } = this.props;
        return (
        <div>
            <IconButton color="inherit" onClick={this.handleClickOpen}>
                <TimelineIcon />
            </IconButton>
            <Dialog
            open={this.state.setOpen}
            onClose={this.handleClose}
            aria-labelledby="alert-dialog-title"
            aria-describedby="alert-dialog-description"
            >
                <IconButton aria-label="close" className={classes.closeButton} onClick={this.handleClose}>
                    <CloseIcon />
                </IconButton>
                <DialogTitle className={classes.heading}>{`Good morning ${this.state.userName},`}</DialogTitle>
                <DialogContent>
                    <DialogContentText>
                        <b>Last week, you spent:<br></br></b>
                        {this.state.social} hours on your Social Life<br></br>
                        {this.state.work} hours on your Work Life<br></br>
                        {this.state.school} hours on your School Life<br></br>
                        {this.state.family} hours on your Family Life
                    </DialogContentText>
                </DialogContent>
            </Dialog>
        </div>
        );
    }
}

export default withStyles(styles)(TimeBreakdown);