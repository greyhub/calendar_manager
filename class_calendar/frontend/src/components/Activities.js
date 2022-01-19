import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import axios from "axios";

const header = ["No","Name", "Created Date", "Start Date", "End Date", "Referral Link"];

class Activities extends Component {
	constructor(props) {
		super(props);

		this.state = {
			number_row: 10,
			number_page: 1,
			activities: [],
			shown: false
		};
		this.displayActivities = this.displayActivities.bind(this);
	}

	 displayActivities(e) {
		e.preventDefault();
		this.setState({shown: true});
		console.log('Show activities!');
		console.log(this.state);
        axios.post('https://ctsv.hust.edu.vn/api-t/Activity/GetPublishActivity',
            {NumberRow: this.state.number_row, PageNumber: this.state.number_page}
		).then(
				response => {
            	console.log("res", response.data);
				this.setState({activities: response.data.Activities});
				}).catch(error => {
				console.log("error", error);
		});
	 }
	render() {
		if (this.state.shown === true){
			console.log("data", this.state.data)
            return (
                <div>
                    <table>
                        <thead>
                        <tr>{header.map((h, i) => <th key={i}>{h}</th>)}</tr>
                        </thead>
                        <tbody>
                        {Object.keys(this.state.activities).map((k, i) => {
                            let data = this.state.activities[k];
                            return (
                                <tr key={i}>
                                    <td>{k}</td>
                                    <td>{data.AName}</td>
                                    <td>{data.CreateDate}</td>
                                    <td>{data.StartTime}</td>
                                    <td>{data.FinishTime}</td>
									<td><a href={`https://ctsv.hust.edu.vn/#/hoat-dong/${data.ACode}/chi-tiet`}>
										link to detail
									</a></td>
                                </tr>
                            );
                        })}
                        </tbody>
                    </table>
					{/* <Link to="/">Login Here</Link> */}
                </div>
            )
		}
		else {
			return (
				<div className="register">
					<form onSubmit={this.displayActivities}>
						<input type="submit" value="Show activities"/>
					</form>

					{/* <Link to="/">Login Here</Link> */}
				</div>
			);
		}
	}
}

export default Activities;
