function signUpPage() {

    return(
        <div className="SignUpPage">
        <h1>Sign Up</h1>
        <form onSubmit={}>
            <label>
                Username:
                <input type="text" name="username" />
            </label>
            <label>
                Email:
                <input type="text" name="email" />
            </label>
            <label>
                First name:
                <input type="text" name="firstname" />
            </label>
            <label>
                Last name:
                <input type="text" name="lastname" />
            </label>
            <label>
                Password:
                <input secureTextEntry="true" type="text" name="pw" />
            </label>
            <button type="submit">Sign Up</button>
        </form>
        </div>

    );
} 

export default signUpPage;