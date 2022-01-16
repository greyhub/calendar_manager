import React, {Component} from 'react';
import {Link} from 'react-router-dom';
import axios from 'axios';

const header = ["STT", "SubjectName", "SubjectId", "ClassID", "TimeStart", "TimeEnd"];


class Login extends Component {
    constructor(props) {
        super(props);

        this.state = {
            email: '',
            password: '',
            data: [],
            isLogin: false
        };


        this.displayLogin = this.displayLogin.bind(this);
    }

    updateEmail = (e) => {
        let value = e.target.value;
        this.setState({
            email: value
        });
        // console.log('value', value)
    }

    updatePassword = (e) => {
        let value = e.target.value;
        this.setState({
            password: value
        })
    }

    displayLogin(e) {
        e.preventDefault();
        console.log(this.state);
        this.setState({
            email: '',
            password: '',
            data: []
        });
        console.log("log state", this.state.email, this.state.password);
        axios.post('https://ctsv.hust.edu.vn/api-t/User/UserLogin/',
            {UserName: this.state.email, Password: this.state.password}).then(response => {
            console.log("res", response.data);

            console.log("token:", response.data.TokenCode);
            let userLogin = response.data;
            axios.post('http://202.191.56.100/UploadFile/CTSV/GetScheduleStudent',
                {UserName: userLogin.Email, TokenCode: userLogin.TokenCode, UserCode: userLogin.UserName}
            ).then(response => {
                console.log('res', response.data);
                this.setState({data: response.data.ScheduleStudentLst});
                this.setState({isLogin: true});
            }).catch(error => {
            });

        }).catch(error => {
            console.log("error", error);
        });
    }

    render() {
        if (this.state.isLogin === true) {
            console.log("data", this.state.data)
            return (
                <div>
                    <table>
                        <thead>
                        <tr>{header.map((h, i) => <th key={i}>{h}</th>)}</tr>
                        </thead>
                        <tbody>
                        {Object.keys(this.state.data).map((k, i) => {
                            let data = this.state.data[k];
                            return (
                                <tr key={i}>
                                    <td>{k}</td>
                                    <td>{data.SubjectName}</td>
                                    <td>{data.SubjectId}</td>
                                    <td>{data.ClassID}</td>
                                    <td>{data.TimeStart}</td>
                                    <td>{data.TimeEnd}</td>
                                </tr>
                            );
                        })}
                        </tbody>
                    </table>
                    <Link to="/activities">Watch list activities</Link>
                </div>
            )
        } else {
            return (
                <div className="login">
                    <form onSubmit={this.displayLogin}>
                        <h2>Login</h2>
                        <div className="username">
                            <input
                                type="text"
                                placeholder="Username..."
                                value={this.state.email}
                                onChange={this.updateEmail}
                                name="email"
                            />
                        </div>

                        <div className="password">
                            <input
                                type="password"
                                placeholder="Password..."
                                value={this.state.password}
                                onChange={this.updatePassword}
                                name="password"
                            />
                        </div>

                        <input type="submit" value="Login"/>
                    </form>

                    <Link to="/activities">Watch list activities.</Link>

                </div>

            );
        }
    }
}

export default Login;
