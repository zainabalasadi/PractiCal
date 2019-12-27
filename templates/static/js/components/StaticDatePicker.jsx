import React, { useState } from "react";
import { DatePicker, MuiPickersUtilsProvider } from '@material-ui/pickers';
import MomentUtils from '@date-io/moment';

const StaticDatePicker = () => {
  const [date, changeDate] = useState(new Date());

  // prettier-ignore
  return (
    <MuiPickersUtilsProvider utils={MomentUtils}>
        <DatePicker 
          autoOk
          orientation="landscape"
          variant="static"
          openTo="date"
          value={date}
          onChange={changeDate}
          disableToolbar={true}
          readOnly={true}
        />
    </MuiPickersUtilsProvider>
    );
};

export default StaticDatePicker;