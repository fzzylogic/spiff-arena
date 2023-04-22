import { Button } from '@carbon/react';

export default function Login() {
  return (
    <div style={{ marginTop: '25px' }}>
      <div
        style={{
          margin: 'auto',
          width: '300px',
          minHeight: '320px',
          background: '#126d82',
          textAlign: 'center',
          borderRadius: '10px',
          border: '1px solid black',
          padding: '20px',
          color: 'white',
        }}
      >
        <img src="/logo192Inverted.png" alt="Spiffworkflow Logo" />
        <h1 style={{ color: 'white', margin: '0px' }}>SpiffWorkflow</h1>
        <p style={{ color: 'white' }}>Log In</p>
        <br />
        <br />
        <Button href="/" style={{ marginBottom: '10px' }}>
          <img
            width="20px"
            alt="Google sign-in"
            src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/512px-Google_%22G%22_Logo.svg.png"
          />
          <span style={{ display: 'inline-block', marginLeft: '10px' }}>
            Sign in with Google
          </span>
        </Button>
      </div>
    </div>
  );
}
