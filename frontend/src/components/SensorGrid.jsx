import { getSensorStatus } from "../utils/helpers";

export default function SensorGrid({ sensors }) {
  const { mq7 = 0, mq135 = 0, mq2 = 0, temp = 0, humidity = 0, flame = false } = sensors;
  const mq7s   = getSensorStatus(mq7,   70,  200);
  const mq135s = getSensorStatus(mq135, 80,  120);
  const mq2s   = getSensorStatus(mq2,   100, 300);

  return (
    <div className="sgrid">
      {/* MQ-7 — full width */}
      <div className="sc wide">
        <div className="sc-top">
          <div>
            <div className="sc-id">MQ-7 Sensor</div>
            <div className="sc-name">Carbon Monoxide</div>
          </div>
          <span className={`chip ${mq7s}`}>{mq7s}</span>
        </div>
        <div className="sc-reading">
          <span className={`sc-val wide ${mq7s}`}>{mq7}</span>
          <span className="sc-unit">ppm</span>
        </div>
      </div>

      {/* MQ-135 */}
      <div className="sc">
        <div className="sc-top">
          <div>
            <div className="sc-id">MQ-135</div>
            <div className="sc-name">Air Quality</div>
          </div>
          <span className={`chip ${mq135s}`}>{mq135s}</span>
        </div>
        <div className="sc-reading">
          <span className={`sc-val ${mq135s}`}>{mq135}</span>
          <span className="sc-unit">ppm</span>
        </div>
      </div>

      {/* MQ-2 */}
      <div className="sc">
        <div className="sc-top">
          <div>
            <div className="sc-id">MQ-2</div>
            <div className="sc-name">Combustibles</div>
          </div>
          <span className={`chip ${mq2s}`}>{mq2s}</span>
        </div>
        <div className="sc-reading">
          <span className={`sc-val ${mq2s}`}>{mq2}</span>
          <span className="sc-unit">ppm</span>
        </div>
      </div>

      {/* DHT22 */}
      <div className="sc">
        <div className="sc-top">
          <div>
            <div className="sc-id">DHT22</div>
            <div className="sc-name">Environment</div>
          </div>
        </div>
        <div className="env-rows">
          <div className="env-row">
            <span className="env-ico">🌡️</span>
            <span className="env-val">{temp}</span>
            <span className="env-u">°C</span>
          </div>
          <div className="env-row">
            <span className="env-ico">💧</span>
            <span className="env-val">{humidity}</span>
            <span className="env-u">%</span>
          </div>
        </div>
      </div>

      {/* Flame Sensor */}
      <div className="sc">
        <div className="sc-top">
          <div>
            <div className="sc-id">Flame Sensor (IR)</div>
            <div className="sc-name">Fire Detection</div>
          </div>
        </div>
        <div className="flame-body">
          <div className="flame-ico">🔥</div>
          <div className={`flame-lbl ${flame ? "cc D" : "cc S"}`}>
            {flame ? "Flame Detected!" : "No Flame Detected"}
          </div>
          <span className={`chip ${flame ? "DANGER" : "SAFE"}`}>
            {flame ? "DANGER" : "SAFE"}
          </span>
        </div>
      </div>
    </div>
  );
}
