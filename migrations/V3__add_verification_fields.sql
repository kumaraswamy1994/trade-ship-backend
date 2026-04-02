-- Add verification fields to trade and transport users
ALTER TABLE trade.trade_users
    ADD COLUMN gst_verified BOOLEAN NOT NULL DEFAULT FALSE,
    ADD COLUMN email_verified BOOLEAN NOT NULL DEFAULT FALSE,
    ADD COLUMN aadhar_verified BOOLEAN NOT NULL DEFAULT FALSE;

ALTER TABLE transport.transport_users
    ADD COLUMN gst_verified BOOLEAN NOT NULL DEFAULT FALSE,
    ADD COLUMN email_verified BOOLEAN NOT NULL DEFAULT FALSE,
    ADD COLUMN aadhar_verified BOOLEAN NOT NULL DEFAULT FALSE;
