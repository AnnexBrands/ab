# Webhooks

```{eval-rst}
.. autoclass:: ab.api.endpoints.webhooks.WebhooksEndpoint
   :members:
   :undoc-members:
```

## Methods

Server-side callback receivers. These endpoints are typically invoked by
external services (Stripe, Twilio), not by SDK consumers directly.

### Stripe

#### handle_stripe / handle_stripe_connect / handle_stripe_checkout

`POST /webhooks/stripe/handle|connect/handle|checkout.session.completed`

### Twilio

#### handle_twilio_body_sms / handle_twilio_form_sms / handle_twilio_status

`POST /webhooks/twilio/body-sms-inbound|form-sms-inbound|smsStatusCallback`
