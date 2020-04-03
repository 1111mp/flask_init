import './styles.styl'

import React, { Component } from 'react'
import { Form, Input, Button, Checkbox } from 'antd'
import { UserOutlined, LockOutlined } from '@ant-design/icons'

export default class Login extends Component<any> {
	onFinish = (value: any) => {
		console.log(value)
	}

	render() {
		return (
			<div className="login-wrapper">
				<Form
					name="normal_login"
					className="login-form"
					initialValues={{ remember: true }}
					onFinish={this.onFinish}
				>
					<Form.Item
						name="username"
						rules={[{ required: true, message: 'Please input your Username!' }]}
					>
						<Input prefix={<UserOutlined className="site-form-item-icon" />} placeholder="Username" />
					</Form.Item>
					<Form.Item
						name="password"
						rules={[{ required: true, message: 'Please input your Password!' }]}
					>
						<Input
							prefix={<LockOutlined className="site-form-item-icon" />}
							type="password"
							placeholder="Password"
						/>
					</Form.Item>
					<Form.Item>
						<Form.Item name="remember" valuePropName="checked" noStyle>
							<Checkbox>Remember me</Checkbox>
						</Form.Item>

						<span className="login-form-forgot">
							Forgot password
        		</span>
					</Form.Item>

					<Form.Item>
						<Button type="primary" htmlType="submit" className="login-form-button">
							Log in
        		</Button>
        Or <span className="register">register now!</span>
					</Form.Item>
				</Form>
			</div>
		)
	}
}