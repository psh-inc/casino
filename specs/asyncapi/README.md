# AsyncAPI Contracts

- smartico-events.yaml - canonical Kafka event contract derived from `casino-b` event classes and publishers.
- casino-core.json - JSON rendering of `smartico-events.yaml` for tool compatibility.

Notes:
- Event payloads include BaseEvent fields plus payload fields when @JsonUnwrapped is used.
